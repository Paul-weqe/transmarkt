import scrapy
from scrapy.crawler import CrawlerProcess
import random

user_agent = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz1234567890@') for i in range(10)))


class FetchDebutantsSpider(scrapy.Spider):
    start_urls = []
    name = None

    def __init__(self, **kwargs):
        scrapy.Spider.__init__(self, name=kwargs['kwargs']['name'])
        self.start_urls = kwargs['kwargs']['start_urls']

    def parse(self, response, **kwargs):
        for row in response.css("div#yw1 table tbody tr.odd, div#yw1 table tbody tr.even"):
            player_link = row.css("td:nth-of-type(1) table td.hauptlink a::attr('href')").get()
            player_name = row.css("td:nth-of-type(1) table td.hauptlink a::text").get()

            yield {
                'name': player_name,
                'link': f"https://www.transfermarkt.co.uk{player_link}"
            }

def fetch_debutants():
    leagues = [
        'https://www.transfermarkt.co.uk/premier-league/profidebuetanten/wettbewerb/GB1/',
        'https://www.transfermarkt.co.uk/championship/profidebuetanten/wettbewerb/GB2',
        'https://www.transfermarkt.co.uk/league-one/profidebuetanten/wettbewerb/GB3',
        'https://www.transfermarkt.co.uk/league-two/profidebuetanten/wettbewerb/GB4',
        'https://www.transfermarkt.co.uk/league-1/profidebuetanten/wettbewerb/FR1',
        'https://www.transfermarkt.co.uk/league-2/profidebuetanten/wettbewerb/FR2',
    ]
    process = CrawlerProcess(settings = {
        "FEEDS": {
            f"json/debutants.json": { "format": "json" }
        },
        "USER_AGENT": user_agent
    })
    process.crawl(FetchDebutantsSpider, kwargs={
        'name': 'Debutants Crawler',
        'start_urls': leagues
    })
    process.start()
