from scrapy.crawler import CrawlerProcess

from src.players.detailed_players_spider import DetailedPlayersSpider, create_db

create_db()
process = CrawlerProcess()
process.crawl(DetailedPlayersSpider)
process.start()