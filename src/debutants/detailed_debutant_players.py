import re
import datetime
from dateutil.relativedelta import relativedelta

import json
import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from src.detailed_players import DetailedPlayersSpider
from src.extensions import SqlContext


ROOT_URL = "https://www.transfermarkt.co.uk"

class DetailedDebutantPlayersSpider(scrapy.Spider):
    start_urls = []
    name = "detailed debutant players spider"
    custom_settings = {
        "FEEDS": {
            f"csv/debutants.csv": {"format": "csv"}
        },
        "USER_AGENT": "Random Agent"
    }
    players_info = None

    def __init__(self):
        scrapy.Spider.__init__(self, name=self.name)
        self.start_urls = self.fetch_urls()

    def fetch_urls(self) -> list:
        links = []

        with open("json/debutants.json") as file:
            file_data = json.load(file)
            self.players_info = file_data
            file.close()

        for x in file_data:
            links.append(x['link'])
        return links

    @staticmethod
    def strip_string(input_):
        if type(input_) is str:
            return input_.strip()
        return input_

    @staticmethod
    def change_currency_to_numbers(number_str: str):
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

    def parse(self, response):
        headline_wrapper = response.css(".data-header__headline-wrapper")
        shirt_number = self.strip_string(headline_wrapper.css("span::text").get())
        beauty_soup = BeautifulSoup(str(headline_wrapper.get()), features='lxml')
        full_name = beauty_soup.get_text()

        if full_name is not None:
            if shirt_number is not None:
                full_name = self.strip_string(full_name.replace(shirt_number, ""))
            else:
                full_name = self.strip_string(full_name)
        for table in response.css("div.info-table"):

            with SqlContext() as sql:

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

                info = {"Name": f"{full_name}", "Date of debut": "", "Date of birth": None, "Place of birth": None, "Age": None,
                        "Height": None, "Position": None, "Foot": None, "Player Agent": None, "Agent Link": None,
                        "Current Club": None, "Joined": None, "Contract Expires": None, "Outfitter": None, "Url": url,
                        "Current Value": current_value, "Max Value": max_value, "Max Value Date": max_value_date,
                        "Last Contract Extension": None, "League Name": league_name, "On Loan": False}

                for player in self.players_info:
                    if player["link"].strip() == url:
                        info["Age At Debut"] = player["age_at_debut"]

                n = 2

                for x in range(0, len(info_spans) - n + 1, n):
                    info_pair = info_spans[x:x + n]
                    title = BeautifulSoup(info_pair[0].strip(), features='lxml').get_text().strip()
                    value = BeautifulSoup(info_pair[1].strip(), features='lxml').get_text().strip()

                    match title:

                        case "Date of birth:":
                            info["Date of birth"] = value

                        case "Place of birth:":
                            info["Place of birth"] = value

                        case "Age:":
                            info["Age"] = value

                        case "Height:":
                            info["Height"] = value

                        case "Citizenship:":
                            info["Citizenship"] = value

                        case "Position:":
                            info["Position"] = value

                        case "Foot:":
                            info["Foot"] = value

                        case "On loan from:":
                            info["On Loan"] = True

                        case "Player agent:":
                            info["Player Agent"] = value

                            agent_link_bs = BeautifulSoup(info_pair[1].strip(), features='lxml').findAll("a", {})
                            if len(agent_link_bs) > 0:
                                link = BeautifulSoup(info_pair[1].strip(), features='lxml').a['href']
                                info["Agent Link"] = f"{ROOT_URL}{link}"

                        case "Current club:":
                            info["Current Club"] = value

                        case "Joined:":
                            info["Joined"] = value

                        case "Contract expires:":
                            info["Contract Expires"] = value

                        case "Outfitter:":
                            info["Outfitter"] = value

                        case "Date of last contract extension:":
                            info["Last Contract Extension"] = value

                date_of_birth = info["Date of birth"]
                age_at_debut = info["Age At Debut"]
                date_of_debut = ""

                if age_at_debut.strip() == "-":
                    date_of_debut = ""
                elif date_of_birth.strip() == "":
                    pass
                else:
                    date_of_birth = datetime.datetime.strptime(date_of_birth.strip(), "%b %d, %Y")
                    years, months, days = 0, 0, 0
                    year_of_debut_str = re.findall('[0-9]+ year', age_at_debut)
                    month_of_debut_str = re.findall('[0-9]+ month', age_at_debut)
                    day_of_debut_str = re.findall('[0-9]+ day', age_at_debut)

                    if len(year_of_debut_str) != 0:
                        years = int(year_of_debut_str[0].split(" ")[0])

                    if len(month_of_debut_str) != 0:
                        months = int(month_of_debut_str[0].split(" ")[0])

                    if len(day_of_debut_str) != 0:
                        days = int(day_of_debut_str[0].split(" ")[0])

                    date_of_debut = date_of_birth + relativedelta(years = years, months = months) \
                                    + datetime.timedelta(days = days)

                    date_of_debut = date_of_debut.strftime("%b %d, %Y")

                info["Date of debut"] = date_of_debut
                current_value = self.strip_string(current_value)
                yield info

def fetch_detailed_debutants():
    with open("json/debutants.json") as file:
        file_data = json.load(file)
        file.close()

    links = []
    for x in file_data:
        links.append(x['link'])

    process = CrawlerProcess()
    process.crawl(DetailedPlayersSpider)
    process.start()

