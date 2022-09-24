import os
import scrapy
from scrapy.crawler import CrawlerProcess


class FetchLeagueSpider(scrapy.Spider):

    start_urls = [
    ]
    league_name = None
    name = None

    def __init__(self, **kwargs):

        scrapy.Spider.__init__(self, name=kwargs['kwargs']['name'])
        self.start_urls = kwargs['kwargs']['start_urls']
        self.league_name = kwargs['kwargs']['league_name']

    def parse(self, response):
        for row in response.css("div#yw1 table tbody tr.odd, div#yw1 table tbody tr.even"):
            name = row.css('td:nth-of-type(2) a::text').get()
            link = row.css('td:nth-of-type(2) a::attr("href")').get()
            json_dirname = f"{os.getcwd()}/json"

            if not os.path.exists(json_dirname):
                os.makedirs(json_dirname)
            
            yield {
                'name': name,
                'link': link,
                'league_name': self.league_name
            }

def run_league(league_infos: list):
    process = CrawlerProcess()
    for league in league_infos:
        process = CrawlerProcess(settings = {
            "FEEDS": {
                f"json/leagues/{league['league_name']}.json": { "format": "json" }
            },
            "USER_AGENT": f"{league['league_name']} agent"
        })
        process.crawl(FetchLeagueSpider, kwargs={
            'league_name': f"{league['league_name']}", 
            'name': f"{league['league_name']}",
            'start_urls': [ f"{league['league_url']}", ]
        })
    process.start()



run_league([
    {'league_name': 'premier-league', 'league_url': 'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1'},
    {'league_name': 'la-liga', 'league_url': 'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1'}
])
