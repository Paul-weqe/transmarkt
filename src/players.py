import json
import pathlib
from pprint import pprint as pp
import os
import scrapy
from scrapy.crawler import CrawlerProcess


class FetchTeamSpider(scrapy.Spider):

    start_urls = [
    ]
    name = None

    def __init__(self, **kwargs):
        super().__init__(name = kwargs['kwargs']['name'], **kwargs)
        self.start_urls = kwargs['kwargs']['start_urls']
    
    def parse(self, response):
        for row in response.css("div#yw1 table tbody tr.odd, div#yw1 table tbody tr.even"):
            name = row.css("td:nth-of-type(2) table td.hauptlink a::text").get()
            link = row.css("td:nth-of-type(2) table td.hauptlink a::attr('href')").get()
            position = row.css("td:nth-of-type(2) table tr:nth-of-type(2) td::text").get()
            
            yield {
                "name": name,
                "link": link,
                "position": position
            }

def fetch_players():
    filename = "json/teams.json"
    leagues_list = []
    with open(filename, "r") as file:
        leagues_list = json.load(file)
    
    process = CrawlerProcess()
    links = []
    for league in leagues_list:
        links.append(f"https://www.transfermarkt.com{league['link']}")
    
    process = CrawlerProcess(settings = {
        "FEEDS": {
            f"json/players.json": {"format": "json"}
        },
        "USER_AGENT": "Random agent"
    })
    process.crawl(FetchTeamSpider, kwargs={
        'start_urls': links,
        'name': "Players"
    })
    process.start()

