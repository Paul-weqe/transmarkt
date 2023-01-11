from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess

# from apps.scraper.spiders.leagues_scraper import LeaguesSpider
from apps.scraper.spiders.players_spider import PlayerSpider

class Command(BaseCommand):
    help = "release the spiders"
    def handle(self, *args, **options):
        process = CrawlerProcess()
        process.crawl(PlayerSpider)
        process.start()

