#!/bin/bash
rm -rf json
rm -rf players.db
rm -rf data.csv
python run.py
python sync_dbs.py
