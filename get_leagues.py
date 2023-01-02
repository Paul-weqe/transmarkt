from scrapy.crawler import CrawlerProcess
from src.players.leagues_spider import FetchLeagueSpider

process = CrawlerProcess()
process.crawl(FetchLeagueSpider)
process.start()

