from scrapy.item import Item, Field

class DebutPlayerItem(Item):
    link = Field()
    name = Field()
    age_at_debut = Field()
