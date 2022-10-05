import csv
import sqlite3
from  src.extensions import SqlContext, FileContext

def fetch_csv(filepath: str):
    with FileContext(filepath) as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)
        info = list(csv_reader)
        return info

def fetch_sqlite3(filepath: str):
    with SqlContext() as sql:
        res = sql.curr.execute("SELECT * FROM players")
        return res.fetchall() 


