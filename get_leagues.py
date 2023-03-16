from scrapy.crawler import CrawlerRunner
from src.players.leagues_spider import FetchLeagueSpider
from src.players.players_spider import FetchTeamSpider
from src.players.detailed_players_spider import DetailedPlayersPlayerBaseSpider


from twisted.internet import reactor, defer

runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    # yield runner.crawl(FetchLeagueSpider)
    # yield runner.crawl(FetchTeamSpider)
    yield runner.crawl(DetailedPlayersPlayerBaseSpider)
    reactor.stop()

crawl()
reactor.run()
