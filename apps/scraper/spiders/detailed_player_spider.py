from scraper.spiders.base_detailed_player_spider import DetailedPlayerBaseSpider
from authentication.models import BasicPlayer, Player
from django.forms import model_to_dict
import scrapy

ROOT_URL = "https://www.transfermarkt.com"

class DetailedPlayerSpider(DetailedPlayerBaseSpider):
    """
    Should be run after the FetchTeamSpider in players_spider.py.
    This fetches more specific details such as club, age, agent information etc.
    """
    start_urls = [ ]
    name = "Detailed Players Crawler"
    custom_settings = {
        "FEEDS": {
            f"json/detailed_players.json": {"format": "json"}
        },
        "USER_AGENT": "Random Agent"
    }

    def __init__(self):

        scrapy.Spider.__init__(self, name=self.name)
        self.start_urls = self.fetch_urls()

    def fetch_urls(self) -> list:
        links = BasicPlayer.objects.values('link')
        links = [f"{ROOT_URL}{x['link']}" for x in links]
        return links


    def parse(self, response, **kwargs):
        info = self.detailed_player(response)
        model_info = Player.objects.filter(url=info['url']).first()
        if model_info is None:
            info.save()
        else:
            old_values = model_to_dict(info)
            old_values.update(info.__dict__['_values'])
            Player.objects.filter(url=info['url']).update(**old_values)
            
        yield info
