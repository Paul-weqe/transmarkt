from unidecode import unidecode
import sqlite3
import scrapy
import json
import os
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from src.extensions import SqlContext, INSERT_SQL

ROOT_URL = "https://www.transfermarkt.com"


class DetailedPlayersSpider(scrapy.Spider):
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

                

                current_value = self.strip_string( response.css(".tm-player-market-value-development__current-value::text").get() )
                current_value = self.change_currency_to_numbers(str(current_value))

                max_value = self.strip_string( response.css(".tm-player-market-value-development__max-value::text").get() )

                max_value_date = self.strip_string( response.css(".tm-player-market-value-development__max div:nth-of-type(3)::text").get() )

                league_name = self.strip_string( response.css('a.data-header__league-link img::attr("title")').get() )

                url = response.request.url
                info_spans = table.css(".info-table__content").extract()

                
                
                info = {"Name": unidecode(f"{full_name}"), "Date of birth": None, "Place of birth": None, "Age": None,
                        "Height": None, "Position": None, "Foot": None, "Player Agent": None, "Agent Link": None,
                        "Current Club": None, "Joined": None, "Contract Expires": None, "Outfitter": None, "Url": url,
                        "Current Value": current_value, "Max Value": max_value, "Max Value Date": max_value_date,
                        "Last Contract Extension": None, "League Name": league_name, "On Loan": False}

                n = 2

                for x in range(0, len(info_spans)-n+1, n):
                    info_pair = info_spans[x:x+n]
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
                

                current_value = self.strip_string( current_value )
                
                sql.curr.execute(INSERT_SQL, (
                    info["Name"], 
                    info["Date of birth"], 
                    info["Place of birth"], 
                    info["Age"], 
                    info["Height"], 
                    info["Citizenship"],
                    info["Position"], 
                    info["Foot"], 
                    info["Player Agent"], 
                    info["Current Club"], 
                    info["Joined"],
                    info["Contract Expires"], 
                    info["Outfitter"], 
                    info["Max Value"],
                    info["Max Value Date"],
                    info["Current Value"],
                    info["Last Contract Extension"],
                    info["Current Club"],
                    info["Url"], 
                    info["League Name"],
                    info["Agent Link"],
                    str(info["On Loan"])
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
    

def fetch_detailed_players():
    links = []

    with open("json/players.json") as file:
        file_data = json.load(file)
        file.close()

    for x in file_data:
        links.append(f"https://www.transfermarkt.com{x['link']}")

    process = CrawlerProcess()
    process.crawl(DetailedPlayersSpider)
    process.start()
