import json
import pathlib
from pprint import pprint as pp
import os
import scrapy
from scrapy.crawler import CrawlerProcess


class FetchTeamSpider(scrapy.Spider):

    start_urls = [
        # "https://www.transfermarkt.com/manchester-city/startseite/verein/281/saison_id/2022",
    ]
    name = None
    team_name = None
    league_name = None

    def __init__(self, **kwargs):
        super().__init__(name = kwargs['kwargs']['name'], **kwargs)
        self.team_name = kwargs['kwargs']['team_name']
        self.start_urls = kwargs['kwargs']['start_urls']
        self.league_name = kwargs['kwargs']['league_name']
    
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


leagues_json = list(pathlib.Path(f"{os.getcwd()}/json/leagues").glob("*.json"))
leagues_list = {}

for league in leagues_json:
    filename = str(league)
    with open(filename, "r") as file:
        full_file_pathname = os.path.splitext(filename)[0]
        league_name = full_file_pathname.split("/")[-1]
        print("." * 20)
        print(leagues_list.keys())
        print(file)
        leagues_list[str(league_name)] = json.load(file)

def run_teams():

    process = CrawlerProcess()
    for league in leagues_list:
        league_info = leagues_list[league]
        for team in league_info:
            team_link = f"https://www.transfermarkt.com{team['link']}"
            team_name = team['name']
            league_name = team['league_name']
            process = CrawlerProcess(settings = {
                "FEEDS": {
                    f"json/teams/{league_name}/{team_name}.json": {"format": "json"}
                },
                "USER_AGENT": f"{team_name} agent"
            })
            process.crawl(FetchTeamSpider, kwargs={
                'start_urls': [team_link,],
                'team_name': team_name,
                'name': team_name,
                'league_name': league_name
            })
    process.start()

# run_teams()


team_name = "AFC Bournemouth"
process = CrawlerProcess(settings = {
    'FEEDS': {
        'bourn.json': {'format': 'json'}
        # f'json/teams/premier-league/{team_name}.json': {"format": "json"}
    },
    "USER_AGENT": "this team agent"
})
process.crawl(FetchTeamSpider, kwargs={
    'start_urls': ['https://www.transfermarkt.com/afc-bournemouth/startseite/verein/989/saison_id/2022',],
    'team_name': team_name,
    'name': team_name,
    'league_name': 'premier-league'
})