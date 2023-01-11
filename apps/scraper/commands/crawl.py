from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess

from apps.scraper.spiders.leagues_scraper import LeaguesSpider

class Command(BaseCommand):
    help = "RELEASE THE SPIDERS"

    def handle(self, *args, **options):
        process = CrawlerProcess()
        process.crawl(LeaguesSpider)
        process.start()

