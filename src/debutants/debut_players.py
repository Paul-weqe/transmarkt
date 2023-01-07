import random
from src.base_spider import BaseTransfermarktSpider
from src.constants import DEBUT_PLAYER_LINKS
from src.items.debut_player_item import DebutPlayerItem


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

            player = DebutPlayerItem()
            player['name'] = row.css("td:nth-of-type(1) table td.hauptlink a::text").get()
            player['link'] = f"https://www.transfermarkt.co.uk{player_link}"
            player['age_at_debut'] = row.css("td:nth-of-type(8)::text").get()
            player['debut_score'] = row.css("td:nth-of-type(7) a span::text").get().strip()
            score_classes = row.css("td:nth-of-type(7) a span").xpath("@class").extract()

            if "greentext" in score_classes:
                player["debut_game_outcome"] = "win"
            elif "redtext" in score_classes:
                player["debut_game_outcome"] = "loss"
            else:
                player["debut_game_outcome"] = "draw"

            yield player
