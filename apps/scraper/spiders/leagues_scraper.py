import scrapy
import random
from apps.scraper.items import TeamItem

user_agent = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz1234567890@') for i in range(10)))

class LeaguesSpider(scrapy.Spider):
    name = "leagues_scraper"
    start_urls = [ 'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1', ]
    custom_settings = {
        "FEEDS": {
            f"json/teams.json": {"format": "json"}
        },
        "USER_AGENT": user_agent
    }

    def parse(self, response, **kwargs):
        for row in response.css("div#yw1 table tbody tr.odd, div#yw1 table tbody tr.even"):
            name = row.css('td:nth-of-type(2) a::text').get()
            link = row.css('td:nth-of-type(2) a::attr("href")').get()


            item = TeamItem()
            item['name'] = name
            item['link'] = link

            yield item