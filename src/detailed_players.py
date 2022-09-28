import scrapy
from scrapy.crawler import CrawlerProcess

ROOT_URL = "https://www.transfermarkt.com"

class DetailedPlayersSpider(scrapy.Spider):
    start_urls = [ ]
    name = None

    def __init__(self, **kwargs):
        scrapy.Spider.__init__(self, name=kwargs['kwargs']['name'])
        self.start_urls = kwargs['kwargs']['start_urls']
    
    def parse(self, response):
        for table in response.css("div.info-table"):
            age = table.css("span:nth-of-type(8)::text").get()
            link = table.css("span:nth-of-type(18) a::attr('href')").get()
            
            current_value = response.css(".tm-player-market-value-development__current-value::text").get()
            max_value = response.css(".tm-player-market-value-development__max-value::text").get()
            max_value_date = response.css(".tm-player-market-value-development__max div:nth-of-type(3)::text").get()


            yield {
                "name": table.css("span:nth-of-type(2)::text").get(),
                "date_of_birth": table.css("span:nth-of-type(4) a::text").get(),
                "place_of_birth": table.css("span:nth-of-type(6) span::text").get(),
                "age": int(age),
                "height": table.css("span:nth-of-type(10)::text").get(),
                "citizenship": table.css("span:nth-of-type(12) img::attr('title')").get(),
                "position": table.css("span:nth-of-type(14)::text").get().strip(),
                "foot": table.css("span:nth-of-type(16)::text").get(),
                "player_agent": table.css("span:nth-of-type(18) a::text").get(),
                "player_agent_link": f"{ROOT_URL}{link}",
                "club": table.css("span:nth-of-type(20) a:nth-of-type(2)::text").get(),
                "joined": table.css("span:nth-of-type(22)::text").get().strip(),
                "contract_expires": table.css("span:nth-of-type(24)::text").get(),
                "last_contract_extension": table.css("span:nth-of-type(26)::text").get(),
                "outfitter": table.css("span:nth-of-type(28)::text").get(),
                "current_value": current_value.strip(),
                "max_value": max_value.strip(),
                "max_value_date": max_value_date.strip()
            }

def fetch_detailed_players():
    process = CrawlerProcess()
    process = CrawlerProcess(settings = {
        "FEEDS": {
            f"json/detailed_players.json": {"format": "json"}
        },
        "USER_AGENT": "Random Agent"
    })
    process.crawl(DetailedPlayersSpider, kwargs={
        'name': "Detailed Players Crawler",
        "start_urls": ["https://www.transfermarkt.com/marc-andre-ter-stegen/profil/spieler/74857"]
    })
    process.start()