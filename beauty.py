from pprint import pprint as pp
import requests
from bs4 import BeautifulSoup
"/unai-simon/profil/spieler/262396"

url = "https://www.transfermarkt.com/unai-simon/profil/spieler/262396"
headers = {
    'User-Agent': 'Custom Agent'
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'lxml')
table = soup.find_all(class_='info-table')[0]
table_content = table.find_all(class_='info-table__content')

TABLE_DETAILS = {
    'NAME_IN_HOME_COUNTRY': table_content[1].string.strip(),
    'DATE_OF_BIRTH': table_content[3].a.string.strip(),
    'PLACE_OF_BIRTH': table_content[5].span.text.strip(),
    'AGE': table_content[7].text.strip(),
    'HEIGHT': table_content[9].string.strip(),
    'CITIZENSHIP': table_content[11].text.strip(),
    'POSITION': table_content[13].text.strip(),
    'FOOT': table_content[15].text.strip(),
    'PLAYER_AGENT': table_content[17].a.string.strip(),
    # COME BACK FOR CLUB
    'DATE_JOINED': table_content[21].string.strip(), # Jul 1, 2018
    'CONTRACT_EXPIRES': table_content[23].text.strip(),
    'LAST_CONTRACT_EXTENSION': table_content[25].text.strip()
}

pp(TABLE_DETAILS)