import scrapy
import random

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
        return [
            'https://www.transfermarkt.co.uk/premier-league/profidebuetanten/wettbewerb/GB1/',
            'https://www.transfermarkt.co.uk/championship/profidebuetanten/wettbewerb/GB2',
            'https://www.transfermarkt.co.uk/league-one/profidebuetanten/wettbewerb/GB3',
            'https://www.transfermarkt.co.uk/league-two/profidebuetanten/wettbewerb/GB4',
            'https://www.transfermarkt.co.uk/league-1/profidebuetanten/wettbewerb/FR1',
            'https://www.transfermarkt.co.uk/league-2/profidebuetanten/wettbewerb/FR2',
            'https://www.transfermarkt.co.uk/bundesliga/profidebuetanten/wettbewerb/L1',
            'https://www.transfermarkt.co.uk/2-bundesliga/profidebuetanten/wettbewerb/L2',
            'https://www.transfermarkt.co.uk/serie-a/profidebuetanten/wettbewerb/IT1',
            'https://www.transfermarkt.co.uk/laliga/profidebuetanten/wettbewerb/ES1',
            'https://www.transfermarkt.co.uk/jupiler-pro-league/profidebuetanten/wettbewerb/BE1',
            'https://www.transfermarkt.co.uk/eredivisie/profidebuetanten/wettbewerb/NL1',
            'https://www.transfermarkt.co.uk/liga-nos/profidebuetanten/wettbewerb/PO1',
            'https://www.transfermarkt.co.uk/premier-liga/profidebuetanten/wettbewerb/UKR1',
            'https://www.transfermarkt.co.uk/premier-liga/profidebuetanten/wettbewerb/RU1',
            'https://www.transfermarkt.co.uk/campeonato-brasileiro-serie-a/profidebuetanten/wettbewerb/BRA1',
            'https://www.transfermarkt.co.uk/superliga/profidebuetanten/wettbewerb/AR1N',
            'https://www.transfermarkt.co.uk/superligaen/profidebuetanten/wettbewerb/DK1',
            'https://www.transfermarkt.co.uk/bundesliga/profidebuetanten/wettbewerb/A1',
            'https://www.transfermarkt.co.uk/allsvenskan/profidebuetanten/wettbewerb/SE1',
            'https://www.transfermarkt.co.uk/eliteserien/profidebuetanten/wettbewerb/NO1',
        ]

    def parse(self, response, **kwargs):
        for row in response.css("div#yw1 table tbody tr.odd, div#yw1 table tbody tr.even"):
            player_link = row.css("td:nth-of-type(1) table td.hauptlink a::attr('href')").get()
            player_name = row.css("td:nth-of-type(1) table td.hauptlink a::text").get()

            yield {
                'name': player_name,
                'link': f"https://www.transfermarkt.co.uk{player_link}"
            }
