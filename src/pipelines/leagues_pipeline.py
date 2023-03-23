import json
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter

class LeaguesPipeline:
    def open_spider(self, spider):
        self.file = open("json/teams.json", "w")
        self.file.write("[" + "\n")
    
    def close_spider(self):
        self.file.write("]")
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + ",\n"
        self.file.write(line)
        return item
