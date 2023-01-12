from scraper.spiders.base_spider import BaseTransfermarktSpider
from authentication.models import Team, BasicPlayer
from scraper.items import PlayerItem, BasicPlayerItem
from django.forms import model_to_dict

import random
BASE_URL = "https://www.transfermarkt.com"
user_agent = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz1234567890@') for i in range(10)))

class PlayerSpider(BaseTransfermarktSpider):
    name = "Fetch Team spider"
    custom_settings = settings = {
        "FEEDS": {
            f"json/players.json": {"format": "json"}
        },
        "USER_AGENT": user_agent
    }

    def fetch_urls(self) -> list:
        links = Team.objects.values('link')
        links = [f"{BASE_URL}{x['link']}" for x in links]
        return links

    def parse(self, response, **kwargs):
        for row in response.css("div#yw1 table tbody tr.odd, div#yw1 table tbody tr.even"):
            name = row.css("td:nth-of-type(2) table td.hauptlink a::text").get()
            link = row.css("td:nth-of-type(2) table td.hauptlink a::attr('href')").get()
            position = row.css("td:nth-of-type(2) table tr:nth-of-type(2) td::text").get()


            item = BasicPlayerItem()
            item['name'] = name
            item['link'] = link
            item['position'] = position

            model_info = BasicPlayer.objects.filter(link=link).first()
            
            if model_info is None:    
                item.save()
            else:
                old_values = model_to_dict(model_info)
                old_values.update(item.__dict__['_values'])
                BasicPlayer.objects.filter(link=link).update(**old_values)
            
            yield item
