"""
Leagues being fetched:
    1. Premier League
    2. Premier League
    3. League 1
    4. League 2
    5. French League 1
    6. French League 2
    7. German Bundersliga
    8. Bundersliga 2
    9. Italy Series A
    10. La Liga
    11. Belgium Jupiter League
    12. Dutch Eredevise
    13. Portugal Premier League
    14. Ukraine Premier League
    15.Russian Premier League
    16. Brazilian League
    17. Argentinian League
    18. Dannish League
    19. Austrian Bundersliga
    20. Swedish league
    21. Norweigian league
    22. Scottish Premier league

Any additions/deletions in leagues being made to any of the constants below, make sure to consider the
above leagues/modify them
"""


LEAGUES_LINKS = [
    'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1', # Premier League
    'https://www.transfermarkt.com/championship/startseite/wettbewerb/GB2',  # League 1
    'https://www.transfermarkt.com/league-one/startseite/wettbewerb/GB3', # League 2
    'https://www.transfermarkt.com/league-two/startseite/wettbewerb/GB4', # League 2
    'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1', # French League 1
    'https://www.transfermarkt.com/ligue-2/startseite/wettbewerb/FR2', # French League 2
    'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1', # German Bundersliga
    'https://www.transfermarkt.com/2-bundesliga/startseite/wettbewerb/L2', # Bundersliga 2
    'https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1', # Italy Series A
    'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1', # La Liga
    'https://www.transfermarkt.com/jupiler-pro-league/startseite/wettbewerb/BE1', # Belgium Jupiter League
    'https://www.transfermarkt.com/eredivisie/startseite/wettbewerb/NL1', # Dutch Eredevise
    'https://www.transfermarkt.com/liga-nos/startseite/wettbewerb/PO1', # Portugal Premier League
    'https://www.transfermarkt.com/premier-liga/startseite/wettbewerb/UKR1', # Ukraine Premier League
    'https://www.transfermarkt.com/premier-liga/startseite/wettbewerb/RU1', # Russian Premier League
    'https://www.transfermarkt.com/campeonato-brasileiro-serie-a/startseite/wettbewerb/BRA1', # Brazilian League
    'https://www.transfermarkt.com/superliga/startseite/wettbewerb/AR1N', # Argentinian League
    'https://www.transfermarkt.com/superligaen/startseite/wettbewerb/DK1', # Dannish League
    'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/A1', # Austrian Bundersliga
    'https://www.transfermarkt.com/allsvenskan/startseite/wettbewerb/SE1', # Swedish league
    'https://www.transfermarkt.com/eliteserien/startseite/wettbewerb/NO1', # Norweigian league
    'https://www.transfermarkt.com/scottish-premiership/startseite/wettbewerb/SC1', # Scottish Premiership
]

DEBUT_PLAYER_LINKS = [
    'https://www.transfermarkt.co.uk/premier-league/profidebuetanten/wettbewerb/GB1/option/profi/plus/1',  # Premier League
    'https://www.transfermarkt.co.uk/championship/profidebuetanten/wettbewerb/GB2/option/profi/plus/1', # Championship
    'https://www.transfermarkt.co.uk/league-one/profidebuetanten/wettbewerb/GB3/option/profi/plus/1', # English League 1
    'https://www.transfermarkt.co.uk/league-two/profidebuetanten/wettbewerb/GB4/option/profi/plus/1', # English League 2
    'https://www.transfermarkt.co.uk/league-1/profidebuetanten/wettbewerb/FR1/option/profi/plus/1', # French League 1
    'https://www.transfermarkt.co.uk/league-2/profidebuetanten/wettbewerb/FR2/option/profi/plus/1', # French League 2
    'https://www.transfermarkt.co.uk/bundesliga/profidebuetanten/wettbewerb/L1/option/profi/plus/1', # German Bundesliga
    'https://www.transfermarkt.co.uk/2-bundesliga/profidebuetanten/wettbewerb/L2/option/profi/plus/1', # Bundesliga 2
    'https://www.transfermarkt.co.uk/serie-a/profidebuetanten/wettbewerb/IT1/option/profi/plus/1', # Italy Series A
    'https://www.transfermarkt.co.uk/laliga/profidebuetanten/wettbewerb/ES1/option/profi/plus/1', # La Liga
    'https://www.transfermarkt.co.uk/jupiler-pro-league/profidebuetanten/wettbewerb/BE1/option/profi/plus/1', # Belgium Jupiter League
    'https://www.transfermarkt.co.uk/eredivisie/profidebuetanten/wettbewerb/NL1/option/profi/plus/1', # Dutch Eredevise
    'https://www.transfermarkt.co.uk/liga-nos/profidebuetanten/wettbewerb/PO1/option/profi/plus/1', # Portugal Premier League
    'https://www.transfermarkt.co.uk/premier-liga/profidebuetanten/wettbewerb/UKR1/option/profi/plus/1', # Ukraine Premier League
    'https://www.transfermarkt.co.uk/premier-liga/profidebuetanten/wettbewerb/RU1/option/profi/plus/1', # Russian Premier League
    'https://www.transfermarkt.co.uk/campeonato-brasileiro-serie-a/profidebuetanten/wettbewerb/BRA1/option/profi/plus/1', # Brazilian League
    'https://www.transfermarkt.co.uk/superliga/profidebuetanten/wettbewerb/AR1N/option/profi/plus/1', # Argentinian League
    'https://www.transfermarkt.co.uk/superligaen/profidebuetanten/wettbewerb/DK1/option/profi/plus/1', # Dannish League
    'https://www.transfermarkt.co.uk/bundesliga/profidebuetanten/wettbewerb/A1/option/profi/plus/1', # Austrian Bundesliga
    'https://www.transfermarkt.co.uk/allsvenskan/profidebuetanten/wettbewerb/SE1/option/profi/plus/1', # Swedish League
    'https://www.transfermarkt.co.uk/eliteserien/profidebuetanten/wettbewerb/NO1/option/profi/plus/1' # Norweigian League
    'https://www.transfermarkt.com/scottish-premiership/wettbewerb/SC1/option/profi/plus/1' # Scottish premier league
]
