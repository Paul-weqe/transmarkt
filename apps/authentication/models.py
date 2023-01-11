from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField()
    link = models.CharField(unique=True)
