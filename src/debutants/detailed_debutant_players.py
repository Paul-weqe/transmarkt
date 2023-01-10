import json
import scrapy
from bs4 import BeautifulSoup
from src.base_spider import BaseTransfermarktSpider
from src.items.detailed_debutant_player_item import DetailedDebutantPlayerItem

ROOT_URL = "https://www.transfermarkt.co.uk"
class DetailedDebutantPlayersSpider(BaseTransfermarktSpider):
    start_urls = []
    name = "detailed debutant players spider"
    custom_settings = {
        "FEEDS": {
            f"csv/debutants.csv": {"format": "csv"}
        },
        "USER_AGENT": "Random Agent"
    }
    players_info = None

    def __init__(self):
        scrapy.Spider.__init__(self, name=self.name)
        self.start_urls = self.fetch_urls()

    def fetch_urls(self) -> list:
        links = []

        with open("json/debutants.json") as file:
            file_data = json.load(file)
            self.players_info = file_data
            file.close()

        for x in file_data:
            links.append(x['link'])
        return links

    def parse(self, response):
        headline_wrapper = response.css(".data-header__headline-wrapper")
        shirt_number = self.strip_string(headline_wrapper.css("span::text").get())
        beauty_soup = BeautifulSoup(str(headline_wrapper.get()), features='lxml')
        full_name = beauty_soup.get_text()

        if full_name is not None:
            if shirt_number is not None:
                full_name = self.strip_string(full_name.replace(shirt_number, ""))
            else:
                full_name = self.strip_string(full_name)
        for table in response.css("div.info-table"):
            current_value = self.strip_string(response.css(".tm-player-market-value-development__current-value a:nth-of-type(1)::text").get())

            if current_value is None:
                current_value = self.strip_string(response.css(".tm-player-market-value-development__current-value::text").get())

            current_value = self.change_currency_to_numbers(str(current_value))
            max_value = self.strip_string(
                response.css(".tm-player-market-value-development__max-value::text").get())
            max_value_date = self.strip_string(
                response.css(".tm-player-market-value-development__max div:nth-of-type(3)::text").get())
            league_name = self.strip_string(response.css('a.data-header__league-link img::attr("title")').get())
            url = response.request.url
            info_spans = table.css(".info-table__content").extract()

            info = DetailedDebutantPlayerItem()
            info.name = full_name
            info.date_of_debut = ""
            info.url = url
            info.current_value = current_value
            info.max_value = max_value
            info.max_value_date = max_value_date
            info.league_name = league_name

            for player in self.players_info:
                if player["link"].strip() == url:
                    info.age_at_debut = player["age_at_debut"]
                    info.debut_score = player["debut_score"]
                    info.debut_outcome = player["debut_game_outcome"]

            n = 2

            for x in range(0, len(info_spans) - n + 1, n):
                info_pair = info_spans[x:x + n]
                title = BeautifulSoup(info_pair[0].strip(), features='lxml').get_text().strip()
                value = BeautifulSoup(info_pair[1].strip(), features='lxml').get_text().strip()

                match title:

                    case "Date of birth:":
                        info.date_of_birth = value

                    case "Place of birth:":
                        info.place_of_birth = value

                    case "Age:":
                        info.age = value

                    case "Height:":
                        info.height = value

                    case "Citizenship:":
                        info.citizenship = value

                    case "Position:":
                        info.position = value

                    case "Foot:":
                        info.foot = value

                    case "On loan from:":
                        info.on_loan = True

                    case "Player agent:":
                        info.player_agent = value

                        agent_link_bs = BeautifulSoup(info_pair[1].strip(), features='lxml').findAll("a", {})
                        if len(agent_link_bs) > 0:
                            link = BeautifulSoup(info_pair[1].strip(), features='lxml').a['href']
                            info.agent_link = f"{ROOT_URL}{link}"

                    case "Current club:":
                        info.current_club = value

                    case "Joined:":
                        info.joined = value

                    case "Contract expires:":
                        info.contract_expires = value

                    case "Outfitter:":
                        info.outfitter = value

                    case "Date of last contract extension:":
                        info.last_contract_extension = value


            yield info

