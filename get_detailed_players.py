from scrapy.crawler import CrawlerProcess

from src.players.detailed_players_spider import DetailedPlayersPlayerBaseSpider, create_db

create_db()
process = CrawlerProcess()
process.crawl(DetailedPlayersPlayerBaseSpider)
process.start()