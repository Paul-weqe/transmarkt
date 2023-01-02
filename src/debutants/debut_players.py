import random
from src.base_spider import BaseTransfermarktSpider
from src.constants import DEBUT_PLAYER_LINKS
user_agent = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz1234567890@') for i in range(10)))

class FetchDebutantsSpider(BaseTransfermarktSpider):
    name = "fetch debutant spider"
    custom_settings = {
        "FEEDS": {
            "json/debutants.json": {"format": "json"}
        },
        "USER_AGENT": user_agent
    }

    def fetch_urls(self) -> list:
        initial_links = DEBUT_PLAYER_LINKS
        paginated_links = []
        for link in initial_links:
            paginated_links += self.get_all_paginated_links(link)
        return paginated_links

    def parse(self, response, **kwargs):
        for row in response.css("div#yw1 table tbody tr.odd, div#yw1 table tbody tr.even"):
            player_link = row.css("td:nth-of-type(1) table td.hauptlink a::attr('href')").get()
            player_name = row.css("td:nth-of-type(1) table td.hauptlink a::text").get()
            age_at_debut = row.css("td:nth-of-type(6)::text").get()

            yield {
                'name': player_name,
                'link': f"https://www.transfermarkt.co.uk{player_link}",
                'age_at_debut': age_at_debut
            }
