from src.merge_csv import fetch_csv, fetch_sqlite3
from src.extensions import SqlContext
from datetime import datetime
from unidecode import unidecode
import csv

csv_path = "initial-data.csv"
db_path = "players.db"
sqlite_players_res = fetch_sqlite3(db_path)

csv_players_res = fetch_csv(csv_path)
players_relations = {}

for player in  sqlite_players_res:

    name = player[0]
    date_of_birth = player[1]

    try:
        dob = datetime.strptime(date_of_birth.strip(), "%b %d, %Y")
    except Exception as e:
        dob = None

    for player2 in csv_players_res:
        csv_name = unidecode(player2[2])
        player_id = player2[15]

        try:
            csv_dob = datetime.strptime(player2[10].strip(), "%Y-%m-%d")
        except Exception as e:
            csv_dob = None


        if name == csv_name and dob == csv_dob:
            players_relations[str(player_id)] = name

new_columns = [
    "date_of_birth", "place_of_birth", "age",
    "height", "citizenship", "position",
    "foot", "player_agent", "player_agent_link",
    "club", "date_joined", "contract_expires",
    "last_contract_extension", "outfitter", "current_value",
    "max_value", "max_value_date", "player_url", "league_name", 
    "on_loan"
]

with open(csv_path) as file_reader, open("data.csv", "w", newline='') as file_writer:
    csv_reader = csv.reader(file_reader, delimiter=',')
    csv_writer = csv.writer(file_writer, delimiter=',')
    counter = 1

    for row in csv_reader:
        if counter == 1:
            row = row + new_columns
            csv_writer.writerow(row)
            counter += 1
            continue

        player_id = row[15]

        player_name = None
        if str(player_id) in players_relations.keys():
            player_name = players_relations[str(player_id)]

        if player_name:
            with SqlContext() as sql:
                player = list( sql.curr.execute("SELECT * FROM players WHERE name=?", (player_name, )).fetchone() )
                del player[0]

                if player:
                    for info in player:
                        row.append(info)

        csv_writer.writerow(row)
