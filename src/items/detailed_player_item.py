from dataclasses import dataclass

@dataclass
class DetailedPlayerItem:
    name: str = None
    date_of_birth: str = None
    place_of_birth: str = None
    age: str = None
    height: str = None
    position: str = None
    citizenship: str = None
    foot: str = None
    player_agent: str = None
    agent_link: str = None
    current_club: str = None
    joined: str = None
    contract_expires: str = None
    outfitter: str = None
    url: str = None
    current_value: str = None
    max_value: str = None
    max_value_date: str = None
    last_contract_extension: str = None
    league_name: str = None
    on_loan: bool = None