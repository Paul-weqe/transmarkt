import logging 
import scrapy
from scrapy.crawler import CrawlerProcess

logging.basicConfig(level = logging.DEBUG)

class FetchLeagueSpider(scrapy.Spider):

    start_urls = [ ]
    name = None

    def __init__(self, **kwargs):

        scrapy.Spider.__init__(self, name=kwargs['kwargs']['name'])
        self.start_urls = kwargs['kwargs']['start_urls']

    def parse(self, response):
        for row in response.css("div#yw1 table tbody tr.odd, div#yw1 table tbody tr.even"):
            name = row.css('td:nth-of-type(2) a::text').get()
            link = row.css('td:nth-of-type(2) a::attr("href")').get()
            
            yield {
                'name': name,
                'link': link
            }

def fetch_leagues():

    leagues = [
        'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1',
        'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1'
    ]

    process = CrawlerProcess()
    process = CrawlerProcess(settings = {
        "FEEDS": {
            f"json/teams.json": { "format": "json" }
        },
        "USER_AGENT": f"Random agent"
    })
    process.crawl(FetchLeagueSpider, kwargs={
        'name': "Leagues Crawler",
        'start_urls': leagues
    })
    process.start()

