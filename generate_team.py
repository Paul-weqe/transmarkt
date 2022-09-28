from pathlib import Path
import logging
import glob
import json
from pprint import pprint as pp
from bs4 import BeautifulSoup
import requests
import os
"/real-madrid/startseite/verein/418/saison_id/2022"

# url = "https://www.transfermarkt.com/real-madrid/startseite/verein/418/saison_id/2022"


def get_players(team_url, team_league, team_name):
    headers  = {
        "User-Agent": "Custom Agent"
    }
    page = requests.get(team_url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find("div", {"id": "yw1"})

    players_table = table.find_all(class_=["odd", "even"])
    players_info = []
    for player in players_table:
        player_a = player.select("td:nth-of-type(2)")[0].find_all("a")[1]
        name = player_a.text
        link = player_a.attrs['href']
        position = player.select("td:nth-of-type(2)")[0].find_all("tr")[1].td.text
        players_info.append(
            {"name": name, "link": link, "position": position}
        )
    players_json = json.dumps(players_info)

    if not os.path.exists("json/teams"):
        os.mkdir("json/teams")
    
    if not os.path.exists(f"json/teams/{team_league}"):
        os.mkdir(f"json/teams/{team_league}")

    with open(f"json/teams/{team_league}/{team_name}.json", "w+") as file:
        file.write(players_json)

leagues_jsons = glob.glob("json/leagues/*.json")
for league_json in leagues_jsons:
    print(league_json)
    league_name = Path(league_json).stem
    with open(league_json) as file:
        info = json.load(file)
        for team in info:
            team_name = team["name"]
            team_path = team["link"]
            league_name = team["league_name"]
            get_players(
                f"https://www.transfermarkt.com{team_path}", 
                team_league = league_name, 
                team_name = team_name
            )
            logging.info(f"Team added {team_name}")


# get_players("https://www.transfermarkt.com/real-madrid/startseite/verein/418/saison_id/2022")