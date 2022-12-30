import scrapy
import random
from src.general import get_all_paginator_links
import _thread

user_agent = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz1234567890@') for i in range(10)))

class FetchDebutantsSpider(scrapy.Spider):
    start_urls = []
    name = "fetch debutant spider"
    custom_settings = {
        "FEEDS": {
            "json/debutants.json": { "format": "json" }
        },
        "USER_AGENT": user_agent
    }
    def __init__(self):
        scrapy.Spider.__init__(self, name=self.name)
        self.start_urls = self.fetch_urls()

    @staticmethod
    def fetch_urls() -> list:
        initial_links = [
            'https://www.transfermarkt.co.uk/premier-league/profidebuetanten/wettbewerb/GB1/option/profi',
            'https://www.transfermarkt.co.uk/championship/profidebuetanten/wettbewerb/GB2/option/profi',
            'https://www.transfermarkt.co.uk/league-one/profidebuetanten/wettbewerb/GB3/option/profi',
            'https://www.transfermarkt.co.uk/league-two/profidebuetanten/wettbewerb/GB4/option/profi',
            'https://www.transfermarkt.co.uk/league-1/profidebuetanten/wettbewerb/FR1/option/profi',
            'https://www.transfermarkt.co.uk/league-2/profidebuetanten/wettbewerb/FR2/option/profi',
            'https://www.transfermarkt.co.uk/bundesliga/profidebuetanten/wettbewerb/L1/option/profi',
            'https://www.transfermarkt.co.uk/2-bundesliga/profidebuetanten/wettbewerb/L2/option/profi',
            'https://www.transfermarkt.co.uk/serie-a/profidebuetanten/wettbewerb/IT1/option/profi',
            'https://www.transfermarkt.co.uk/laliga/profidebuetanten/wettbewerb/ES1/option/profi',
            'https://www.transfermarkt.co.uk/jupiler-pro-league/profidebuetanten/wettbewerb/BE1/option/profi',
            'https://www.transfermarkt.co.uk/eredivisie/profidebuetanten/wettbewerb/NL1/option/profi',
            'https://www.transfermarkt.co.uk/liga-nos/profidebuetanten/wettbewerb/PO1/option/profi',
            'https://www.transfermarkt.co.uk/premier-liga/profidebuetanten/wettbewerb/UKR1/option/profi',
            'https://www.transfermarkt.co.uk/premier-liga/profidebuetanten/wettbewerb/RU1/option/profi',
            'https://www.transfermarkt.co.uk/campeonato-brasileiro-serie-a/profidebuetanten/wettbewerb/BRA1/option/profi',
            'https://www.transfermarkt.co.uk/superliga/profidebuetanten/wettbewerb/AR1N/option/profi',
            'https://www.transfermarkt.co.uk/superligaen/profidebuetanten/wettbewerb/DK1/option/profi',
            'https://www.transfermarkt.co.uk/bundesliga/profidebuetanten/wettbewerb/A1/option/profi',
            'https://www.transfermarkt.co.uk/allsvenskan/profidebuetanten/wettbewerb/SE1/option/profi',
            'https://www.transfermarkt.co.uk/eliteserien/profidebuetanten/wettbewerb/NO1/option/profi',
            'https://www.transfermarkt.co.uk/allsvenskan/profidebuetanten/wettbewerb/SE1/option/profi',
        ]
        paginated_links = []

        for link in initial_links:
            # new_links = _thread.start_new_thread(get_all_paginator_links, link)
            # print(new_links)
            paginated_links += get_all_paginator_links(link)

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





