from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from scrapy.crawler import CrawlerProcess

from src.debutants.debut_players import FetchDebutantsSpider

class HomeView(TemplateView):
    template_name = 'index.html'

class DebutView(View):
    def get(self, request, *args, **kwargs):
        process = CrawlerProcess()
        process.crawl(FetchDebutantsSpider)
        process.start()
        return render(request, 'debut.html', {})