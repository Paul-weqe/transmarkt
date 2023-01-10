import scrapy
import random
import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

from src.items.detailed_debutant_player_item import DetailedDebutantPlayerItem
from src.items.detailed_player_item import DetailedPlayerItem

ROOT_URL = "https://www.transfermarkt.co.uk"

class BaseTransfermarktSpider(ABC, scrapy.Spider):
    name = "Base Transfermarkt"
    start_urls = [ ]
    user_agent = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz1234567890@') for i in range(10)))

    def __init__(self):
        scrapy.Spider.__init__(self, name=self.name)
        self.start_urls = self.fetch_urls()
    @abstractmethod
    def fetch_urls(self) -> list:
        ...

    @abstractmethod
    def parse(self, response, **kwargs):
        ...

    @staticmethod
    def strip_string(input_):
        if type(input_) is str:
            return input_.strip()
        return input_

    @staticmethod
    def change_currency_to_numbers(number_str: str) -> str:
        currency = number_str[0]

        if number_str[-1:] == ".":
            number_str = number_str[:-1]

        letter_representation = number_str[-1:]
        if letter_representation == "m":
            number = float(number_str[1:-1]) * 1_000_000
            return f"{currency}{number}"

        letter_representation = number_str[-2:]
        if letter_representation == "Th":
            number = float(number_str[1:-2]) * 1_000
            return f"{currency}{number}"

        return number_str

    @staticmethod
    def get_all_paginated_links(link) -> list:
        BASE_URL = "https://www.transfermarkt.co.uk"
        agent = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz1234567890@') for i in range(10)))
        response = requests.get(link, headers={'User-Agent': agent})
        soup = BeautifulSoup(response.content, 'html.parser')

        list_links = soup.select(
            ".tm-pagination__list-item:not(.tm-pagination__list-item--icon-first-page)"
            ":not(.tm-pagination__list-item--icon-previous-page)"
            ":not(.tm-pagination__list-item--icon-next-page)"
            ":not(.tm-pagination__list-item--icon-last-page)"
        )

        links = []
        if len(list_links) == 0:
            return [link]

        for link in list_links:
            l = link.find_all('a')[0].get('href')
            links.append(f"{BASE_URL}{l}")
        return links

    def detailed_player(self, response) -> DetailedPlayerItem:
        headline_wrapper = response.css(".data-header__headline-wrapper")
        shirt_number = self.strip_string(headline_wrapper.css("span::text").get())
        beautiful_soup = BeautifulSoup(str(headline_wrapper.get()), features='lxml')
        full_name = beautiful_soup.get_text()

        if full_name is not None:
            if shirt_number is not None:
                full_name = self.strip_string(full_name.replace(shirt_number, ""))
            else:
                full_name = self.strip_string(full_name)

        for table in response.css("div.info-table"):
            current_value = self.strip_string(
                response.css(".tm-player-market-value-development__current-value a:nth-of-type(1)::text").get())

            if current_value is None:
                current_value = self.strip_string(
                    response.css(".tm-player-market-value-development__current-value::text").get())

            current_value = self.change_currency_to_numbers(str(current_value))
            max_value = self.strip_string(
                response.css(".tm-player-market-value-development__max-value::text").get())
            max_value_date = self.strip_string(
                response.css(".tm-player-market-value-development__max div:nth-of-type(3)::text").get())
            league_name = self.strip_string(response.css('a.data-header__league-link img::attr("title")').get())
            url = response.request.url
            info_spans = table.css(".info-table__content").extract()

            info = DetailedDebutantPlayerItem()
            info.name = full_name
            info.date_of_debut = ""
            info.url = url
            info.current_value = current_value
            info.max_value = max_value
            info.max_value_date = max_value_date
            info.league_name = league_name

            n = 2

            for x in range(0, len(info_spans) - n + 1, n):
                info_pair = info_spans[x:x + n]
                title = BeautifulSoup(info_pair[0].strip(), features='lxml').get_text().strip()
                value = BeautifulSoup(info_pair[1].strip(), features='lxml').get_text().strip()

                match title:

                    case "Date of birth:":
                        info.date_of_birth = value

                    case "Place of birth:":
                        info.place_of_birth = value

                    case "Age:":
                        info.age = value

                    case "Height:":
                        info.height = value

                    case "Citizenship:":
                        info.citizenship = value

                    case "Position:":
                        info.position = value

                    case "Foot:":
                        info.foot = value

                    case "On loan from:":
                        info.on_loan = True

                    case "Player agent:":
                        info.player_agent = value

                        agent_link_bs = BeautifulSoup(info_pair[1].strip(), features='lxml').findAll("a", {})
                        if len(agent_link_bs) > 0:
                            link = BeautifulSoup(info_pair[1].strip(), features='lxml').a['href']
                            info.agent_link = f"{ROOT_URL}{link}"

                    case "Current club:":
                        info.current_club = value

                    case "Joined:":
                        info.joined = value

                    case "Contract expires:":
                        info.contract_expires = value

                    case "Outfitter:":
                        info.outfitter = value

                    case "Date of last contract extension:":
                        info.last_contract_extension = value

            return info

