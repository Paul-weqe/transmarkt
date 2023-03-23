from src.constants import LEAGUES_LINKS
from src.base.base_spider import BaseTransfermarktSpider
import random

user_agent = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz1234567890@') for i in range(10)))

class FetchLeagueSpider(BaseTransfermarktSpider):
    """
    Collects all the teams in the leagues whose link is in src/constant.py

    How to run:
    process = CrawlerProcess()
    process.crawl(FetchLeagueSpider)
    process.start()

    NOTE:
        - This does not have any spider/script that is required to run before it.
        - FetchTeamSpider in players_spider.py is usually run after this. This is used to fetch
            general information about the players from transfermarkt website.
    """
    custom_settings = {
        "FEEDS": {
            f"json/teams.json": {"format": "json"}
        },
        "USER_AGENT": user_agent
    }
    name = "Fetch League Spider"

    def parse(self, response, **kwargs):
        for row in response.css("div#yw1 table tbody tr.odd, div#yw1 table tbody tr.even"):
            name = row.css('td:nth-of-type(2) a::text').get()
            link = row.css('td:nth-of-type(2) a::attr("href")').get()

            yield {
                'name': name,
                'link': link
            }

    def fetch_urls(self) -> list:

        result = []
        for x in LEAGUES_LINKS:
            result.append(x['link'])
            
        return result

