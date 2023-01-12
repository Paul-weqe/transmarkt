from scrapy_djangoitem import DjangoItem
from authentication.models import Team, Player, BasicPlayer

class TeamItem(DjangoItem):
    django_model = Team

class BasicPlayerItem(DjangoItem):
    django_model = BasicPlayer

class PlayerItem(DjangoItem):
    django_model = Player