import json
import scrapy
from src.base.base_detailed_player_spider import DetailedPlayerBaseSpider

ROOT_URL = "https://www.transfermarkt.co.uk"
class DetailedDebutantPlayersSpider(DetailedPlayerBaseSpider):
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

    def parse(self, response, **kwargs):
        yield self.detailed_player(response, debutant=True)
