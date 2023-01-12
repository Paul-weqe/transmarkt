import scrapy
import random
from authentication.models import Team
from apps.scraper.items import TeamItem
from django.forms import model_to_dict

user_agent = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz1234567890@') for i in range(10)))

class LeaguesSpider(scrapy.Spider):
    name = "leagues_scraper"
    start_urls = [ 'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1', ]
    custom_settings = {
        "USER_AGENT": user_agent
    }

    def parse(self, response, **kwargs):
        for row in response.css("div#yw1 table tbody tr.odd, div#yw1 table tbody tr.even"):
            name = row.css('td:nth-of-type(2) a::text').get()
            link = row.css('td:nth-of-type(2) a::attr("href")').get()

            item = TeamItem()
            item['name'] = name
            item['link'] = link
            model_info = Team.objects.filter(link=link).first()

            if model_info is None:
                item.save()
            else:
                # update the existing team if it already exists
                old_values = model_to_dict(model_info)
                old_values.update(item.__dict__['_values'])
                Team.objects.filter(link=link).update(**old_values)

            yield None

