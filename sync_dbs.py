from src.extensions import SqlContext, fetch_sqlite3, fetch_csv
from datetime import datetime
from unidecode import unidecode
import csv
import os

csv_path = "initial-data.csv"

sqlite_players_res = fetch_sqlite3()
csv_players_res = fetch_csv(csv_path)

players_relations = {}

for sqlite_player in  sqlite_players_res:

    sql_name = sqlite_player[0]
    sql_dob = sqlite_player[1]
    sql_club = unidecode(sqlite_player[10].strip()) # remove any accents from the name
    sql_nationalities = sqlite_player[5].split(",")
    sql_nationalities = [unidecode(x.strip()) for x in sql_nationalities]
    sql_url = sqlite_player[18]

    try:
        sql_dob = datetime.strptime(sql_dob.strip(), "%b %d, %Y")
    except Exception as e:
        sql_dob = None

    for csv_player in csv_players_res:
        statsbomb_name = unidecode(csv_player[2])
        statsbomb_player_id = csv_player[15]
        statsbomb_club = unidecode(csv_player[3].strip())
        statsbomb_nationality = unidecode(csv_player[8].strip())

        try:
            statsbomb_dob = datetime.strptime(csv_player[10].strip(), "%Y-%m-%d")
        except Exception as e:
            statsbomb_dob = None

        if sql_name == statsbomb_name and sql_dob == statsbomb_dob:
            players_relations[str(statsbomb_player_id)] = sql_url

        elif statsbomb_club in sql_club and sql_dob == statsbomb_dob:
            players_relations[str(statsbomb_player_id)] = sql_url

        elif statsbomb_nationality in sql_nationalities and sql_dob == statsbomb_dob:
            players_relations[str(statsbomb_player_id)] = sql_url


new_columns = [
    "date_of_birth", "place_of_birth", "age",
    "height", "citizenship", "position",
    "foot", "player_agent", "player_agent_link",
    "club", "date_joined", "contract_expires",
    "last_contract_extension", "outfitter", "current_value",
    "max_value", "max_value_date", "player_url", "league_name", 
    "on_loan"
]


if not os.path.exists("csv/"):
    os.makedirs("csv")
with open(csv_path) as file_reader, open("csv/data.csv", "w", newline='') as file_writer:
    csv_reader = csv.reader(file_reader, delimiter=',')
    csv_writer = csv.writer(file_writer, delimiter=',')
    counter = 1

    for row in csv_reader:

        if counter == 1:
            row = row + new_columns
            csv_writer.writerow(row)
            counter += 1
            continue

        statsbomb_player_id = row[15]

        url = None
        if str(statsbomb_player_id) in players_relations.keys():
            url = players_relations[str(statsbomb_player_id)]

        if url:
            with SqlContext() as sql:
                sqlite_player = list(sql.curr.execute("SELECT * FROM players WHERE url=?", (url,)).fetchone())
                del sqlite_player[0]

                if sqlite_player:
                    for info in sqlite_player:
                        row.append(info)

        csv_writer.writerow(row)
