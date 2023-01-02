"""
This players package contains scripts learnt to collect general player information
from leagues listed in src/constants.py file.

There is an order in which the files should be run:
1. leagues_spider.py -> collects the teams in all the leagues
2. players_spider.py -> collects general metadata about players e.g their links etc
3. detailed_players_spider.py -> collects very specific metadata about players e.g dob, player agent, contract information etc.
"""