from scrapy.crawler import CrawlerProcess
from src.players.league import FetchLeagueSpider

process = CrawlerProcess()
process.crawl(FetchLeagueSpider)
process.start()

