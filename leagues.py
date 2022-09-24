from importlib.resources import path
from scrapy.crawler import CrawlerProcess
import pathlib
import os
import json
from pprint import pprint as pp

leagues_json = list(pathlib.Path(f"{os.getcwd()}/json/leagues").glob("*.json"))
leagues_list = {}

for league in leagues_json:
    filename = str(league)
    with open(filename) as file:
        full_file_pathname = os.path.splitext(filename)[0]
        league_name = full_file_pathname.split("/")[-1]
        leagues_list[league_name] = json.load(file)

for league in leagues_list:
    league_info = leagues_list[league]
    process = CrawlerProcess()
    for team in league_info:
        team_link = f"https://www.transfermarkt.com{team['link']}"
        team_name = team['name']