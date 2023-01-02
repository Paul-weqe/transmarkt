import json
from scrapy.crawler import CrawlerProcess
from src.base_spider import BaseTransfermarktSpider
import random

user_agent = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz1234567890@') for i in range(10)))

class FetchTeamSpider(BaseTransfermarktSpider):
    name = "Fetch Team spider"
    custom_settings = settings = {
        "FEEDS": {
            f"json/players.json": {"format": "json"}
        },
        "USER_AGENT": user_agent
    }

    def fetch_urls(self) -> list:
        filename = "json/teams.json"
        with open(filename, "r") as file:
            leagues_list = json.load(file)

        links = []
        for league in leagues_list:
            links.append(f"https://www.transfermarkt.com{league['link']}")
        return links

    def parse(self, response, **kwargs):
        for row in response.css("div#yw1 table tbody tr.odd, div#yw1 table tbody tr.even"):
            name = row.css("td:nth-of-type(2) table td.hauptlink a::text").get()
            link = row.css("td:nth-of-type(2) table td.hauptlink a::attr('href')").get()
            position = row.css("td:nth-of-type(2) table tr:nth-of-type(2) td::text").get()

            yield {
                "name": name,
                "link": link,
                "position": position
            }


def fetch_players():
    process = CrawlerProcess()
    process.crawl(FetchTeamSpider)
    process.start()

