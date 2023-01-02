from dataclasses import dataclass
import sqlite3
import csv

"""
this file will be used to create context managers whenever needed 
to connect to either databases, files etc...
"""

@dataclass
class SQL:
    conn: sqlite3.Connection
    curr: sqlite3.Cursor


class FileContext(object):
    def __init__(self, file_path, action='r'):
        self.file_obj = open(file_path, action)

    def __enter__(self):
        return self.file_obj

    def __exit__(self, type, value, traceback):
        self.file_obj.close()
        return True


class SqlContext(object):
    def __init__(self):
        self.connect = sqlite3.connect("players.db")
        self.cursor = self.connect.cursor()

    def __enter__(self):
        return SQL(conn=self.connect, curr=self.cursor)

    def __exit__(self, type, value, traceback):
        self.connect.close()
        return True


INSERT_SQL = """
INSERT INTO players( 
    name, date_of_birth, place_of_birth, 
    age, height, citizenship, 
    position, foot, player_agent, 
    club, date_joined, contract_expires, 
    outfitter, max_value, max_value_date, 
    current_value, last_contract_extension, club, 
    url, league_name, player_agent_link, on_loan) VALUES (
        ?, ?, ?, 
        ?, ?, ?, 
        ?, ?, ?, 
        ?, ?, ?, 
        ?, ?, ?,
        ?, ?, ?,
        ?, ?, ?,
        ?
    ) 
"""


def fetch_csv(filepath: str):
    with FileContext(filepath) as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)
        info = list(csv_reader)
        return info

def fetch_sqlite3():
    with SqlContext() as sql:
        res = sql.curr.execute("SELECT * FROM players")
        return res.fetchall()
