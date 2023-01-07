from scrapy.item import Item, Field

class DebutPlayerItem(Item):
    name = Field()
    link = Field()
    age_at_debut = Field()
    debut_score = Field()
    first_game_outcome = Field()