#!/bin/bash
rm -rf json
rm -rf players.db
rm -rf data.csv
python get_leagues.py
python get_players.py
python get_detailed_players.py
python sync_dbs.py
