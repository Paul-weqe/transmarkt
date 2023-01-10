from src.items.detailed_player_item import DetailedPlayerItem
from dataclasses import dataclass

@dataclass
class DetailedDebutantPlayerItem(DetailedPlayerItem):
    date_of_debut: str = None
    debut_score: str = None
    debut_outcome: str = None
    age_at_debut: str = None
