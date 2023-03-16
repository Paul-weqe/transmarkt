import sqlite3
import scrapy
import json
import os

from src.base.base_detailed_player_spider import DetailedPlayerBaseSpider
from src.extensions import SqlContext, INSERT_SQL

ROOT_URL = "https://www.transfermarkt.com"

class DetailedPlayersPlayerBaseSpider(DetailedPlayerBaseSpider):
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
        "USER_AGENT": "Random Agent",
    }

    def __init__(self):

        scrapy.Spider.__init__(self, name=self.name)
        self.start_urls = self.fetch_urls()

    def fetch_urls(self) -> list:
        links = []

        with open("json/players.json") as file:
            file_data = json.load(file)
            file.close()

        for x in file_data:
            links.append(f"https://www.transfermarkt.com{x['link']}")

        return links


    def parse(self, response, **kwargs):
        info = self.detailed_player(response)
        with SqlContext() as sql:
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
    
