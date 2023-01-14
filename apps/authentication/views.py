from ast import Dict
from typing import Any
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from scrapy.crawler import CrawlerProcess
from authentication.models import Team
from src.debutants.debut_players import FetchDebutantsSpider

class HomeView(TemplateView):
    template_name = 'index.html'
    

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        teams = Team.objects.all()
        context['teams'] = teams
        return context

class DebutView(View):
    def get(self, request, *args, **kwargs):
        # process = CrawlerProcess()
        # process.crawl(FetchDebutantsSpider)
        # process.start()
        teams = Team.objects.all()
        return render(request, 'debut.html', {'teams': teams})