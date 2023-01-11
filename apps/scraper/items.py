from scrapy_djangoitem import DjangoItem
from authentication.models import Team, Player

class TeamItem(DjangoItem):
    django_model = Team

class PlayerItem(DjangoItem):
    django_model = Player