from scrapy.item import Item, Field
from dataclasses import dataclass

@dataclass
class DebutPlayerItem:
    name: str = None
    link: str = None
    age_at_debut: str = None
    debut_score: str = None
    debut_game_outcome: str = None
    debut_date: str = None