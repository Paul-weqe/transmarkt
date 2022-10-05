import scrapy
from scrapy.crawler import CrawlerProcess

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
        'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1', # Premier League
        'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB2' #Championship
        'https://www.transfermarkt.com/league-one/startseite/wettbewerb/GB3', # League 1
        'https://www.transfermarkt.com/league-one/startseite/wettbewerb/GB4', # League 2
        'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1', # French League 1
        'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR2', # French League 2
        'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1', # German Bundersliga
        'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L2', # Bundersliga 2
        'https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1', # Italy Series A
        'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1', # La Liga
        'https://www.transfermarkt.com/jupiler-pro-league/startseite/wettbewerb/BE1', # Belgium Jupiter League
        'https://www.transfermarkt.com/eredivisie/startseite/wettbewerb/NL1', # Dutch Eredevise
        'https://www.transfermarkt.com/liga-nos/startseite/wettbewerb/PO1', # Portugal Premier League
        'https://www.transfermarkt.com/premier-liga/startseite/wettbewerb/UKR1', # Ukraine Premier League
        'https://www.transfermarkt.com/premier-liga/startseite/wettbewerb/RU1', # Russian Premier League
        'https://www.transfermarkt.com/campeonato-brasileiro-serie-a/startseite/wettbewerb/BRA1', # Brazilian League
        'https://www.transfermarkt.com/superliga/startseite/wettbewerb/AR1N', # Argentinian League
        'https://www.transfermarkt.com/superligaen/startseite/wettbewerb/DK1', # Dannish League
        'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/A1', # Austrian Bundersliga
        'https://www.transfermarkt.com/allsvenskan/startseite/wettbewerb/SE1', # Swedish league
        'https://www.transfermarkt.com/eliteserien/startseite/wettbewerb/NO1', # Norweigian league
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

