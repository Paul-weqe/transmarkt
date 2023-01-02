from scrapy.crawler import CrawlerProcess
from src.players.players_spider import FetchTeamSpider

process = CrawlerProcess()
process.crawl(FetchTeamSpider)
process.start()