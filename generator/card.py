from utils.tiers import get_tier_name
from utils import config


class Card:

    def __init__(self, name: str, cost: int, tier: int, amount: int,
                 picture_file_name: str, description: str, flavour: str):
        self.name = name
        self.cost = cost
        self.tier = tier
        self.amount = amount
        self.picture_file_name = picture_file_name
        self.description = description
        self.flavour = flavour
        self.card_image_full_path = None

    def get_card_file_name(self):
        file_name = f"{get_tier_name(self.tier)}_{self.name.lower().replace(' ', '_')}"
        for forbidden_char in config.FORBIDDEN_CHARACTERS:
            file_name = file_name.replace(forbidden_char, '')
        return file_name