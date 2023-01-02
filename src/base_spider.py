import scrapy
import random
import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
class BaseTransfermarktSpider(ABC, scrapy.Spider):
    name = "Base Transfermarkt"
    start_urls = [ ]
    user_agent = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz1234567890@') for i in range(10)))

    def __init__(self):
        scrapy.Spider.__init__(self, name=self.name)
        self.start_urls = self.fetch_urls()
    @abstractmethod
    def fetch_urls(self) -> list:
        pass

    @abstractmethod
    def parse(self, response, **kwargs):
        pass

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

