from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=500)
    link = models.URLField(unique=True, max_length=600)



class Player(models.Model):
    name = models.CharField(max_length=500, null=True)
    date_of_birth = models.CharField(max_length=50, null=True)
    place_of_birth = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True)
    height = models.CharField(max_length=20, null=True)
    position = models.CharField(max_length=25, null=True)
    citizenship = models.CharField(max_length=200, null=True)
    foot = models.CharField(max_length=30, null=True)
    player_agent = models.CharField(max_length=200, null=True)
    agent_link = models.URLField(max_length=600, null=True)
    current_club = models.CharField(max_length=50, null=True)
    joined = models.CharField(max_length=50, null=True)
    contract_expires = models.CharField(max_length=50, null=True)
    outfitter = models.CharField(max_length=300, null=True)
    url = models.URLField(max_length=500, unique=True, null=True)
    current_value = models.CharField(max_length=30, null=True)
    max_value = models.CharField(max_length=100, null=True)
    max_value_date = models.CharField(max_length=50, null=True)
    last_contract_extension = models.CharField(max_length=50, null=True)
    league_name = models.CharField(max_length=50, null=True)
    on_loan = models.BooleanField(default=False, null=True)



