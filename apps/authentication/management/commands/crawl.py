from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess

from apps.scraper.spiders.leagues_scraper import LeaguesSpider
from apps.scraper.spiders.players_spider import PlayerSpider
from apps.scraper.spiders.detailed_player_spider import DetailedPlayerSpider

class Command(BaseCommand):
    help = "release the spiders"
    def handle(self, *args, **options):
        process = CrawlerProcess()
        # process.crawl(PlayerSpider)
        # process.crawl(LeaguesSpider)
        process.crawl(DetailedPlayerSpider)
        process.start()
