from unidecode import unidecode
import sqlite3
import scrapy
import json
import os
from bs4 import BeautifulSoup
from src.extensions import SqlContext, INSERT_SQL
from src.items.detailed_player_item import DetailedPlayerItem

ROOT_URL = "https://www.transfermarkt.com"

class DetailedPlayersSpider(scrapy.Spider):

    """
    Should be run after the FetchTeamSpider in players_spider.py.
    This fetches more specific details such as club, age, agent information etc.
    """
    start_urls = [ ]
    name = "Detailed Players Crawler"
    custom_settings = {
        "FEEDS": {
            f"json/detailed_players.json": {"format": "json"}
        },
        "USER_AGENT": "Random Agent"
    }

    def __init__(self):

        scrapy.Spider.__init__(self, name=self.name)
        self.start_urls = self.fetch_urls()

    @staticmethod
    def fetch_urls() -> list:
        links = []

        with open("json/players.json") as file:
            file_data = json.load(file)
            file.close()

        for x in file_data:
            links.append(f"https://www.transfermarkt.com{x['link']}")

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

                current_value = self.strip_string( response.css(".tm-player-market-value-development__current-value a:nth-of-type(1)::text").get() )

                if current_value is None:
                    current_value = self.strip_string(response.css(".tm-player-market-value-development__current-value::text").get())
                current_value = self.change_currency_to_numbers(str(current_value))
                max_value = self.strip_string( response.css(".tm-player-market-value-development__max-value::text").get() )
                max_value_date = self.strip_string( response.css(".tm-player-market-value-development__max div:nth-of-type(3)::text").get() )
                league_name = self.strip_string( response.css('a.data-header__league-link img::attr("title")').get() )

                url = response.request.url
                info_spans = table.css(".info-table__content").extract()

                info = DetailedPlayerItem()
                info.url = url
                info.on_loan = False
                info.league_name = league_name
                info.max_value = max_value
                info.current_value = current_value
                info.name = unidecode(full_name)
                info.max_value_date = max_value_date

                n = 2

                for x in range(0, len(info_spans)-n+1, n):
                    info_pair = info_spans[x:x+n]
                    title = BeautifulSoup(info_pair[0].strip(), features='lxml').get_text().strip()
                    value = BeautifulSoup(info_pair[1].strip(), features='lxml').get_text().strip()

                    match unidecode(title):
                        
                        case "Date of birth:":
                            value = value.replace("Happy Birthday", "")
                            info.date_of_birth = value
                    
                        case "Place of birth:":
                            info.place_of_birth = value
                        
                        case "Age:":
                            info.age = value

                        case "Height:":
                            info.height = value
                        
                        case "Citizenship:":
                            value_span = info_pair[1]
                            soup = BeautifulSoup(value_span, 'html.parser')
                            soup_countries = soup.select('.flaggenrahmen')

                            countries = []
                            for country in soup_countries:
                                countries.append(country['title'])

                            info.citizenship = ", ".join(countries)
                        
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
                        
                        case "Letzte Verlangerung:":
                            info.last_contract_extension = value

                current_value = self.strip_string( current_value )
                info.current_value = current_value
                sql.curr.execute(INSERT_SQL, (
                    info.name,
                    info.date_of_birth,
                    info.place_of_birth,
                    info.age,
                    info.height,
                    info.citizenship,
                    info.position,
                    info.foot,
                    info.player_agent,
                    info.current_club,
                    info.joined,
                    info.contract_expires,
                    info.outfitter,
                    info.max_value,
                    info.max_value_date,
                    info.current_value,
                    info.last_contract_extension,
                    info.current_club,
                    info.url,
                    info.league_name,
                    info.agent_link,
                    str(info.on_loan)
                ))
                sql.conn.commit()
                sql.conn.close()

                yield info



def create_db():
    if not os.path.isfile("players.db"):
        con = sqlite3.connect("players.db")
        sql_command = """
            CREATE TABLE players(
                name, date_of_birth, place_of_birth, 
                age, height, citizenship, 
                position, foot, player_agent, 
                player_agent_link, club, date_joined,
                contract_expires, last_contract_extension, outfitter, 
                current_value, max_value, max_value_date,
                url, league_name, on_loan
            )
        """
        cur = con.cursor()
        cur.execute(sql_command)
    
