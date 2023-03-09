import os
from utils import config
from utils.tiers import get_tier_name
from generator.cards import generate_card
from generator.card import Card


class Generator:

    def __init__(self):
        self.cards = []

    def add_card(self, card: Card):
        self.cards.append(card)

    def generate_cards(self):
        for card in self.cards:
            tier_path = os.path.join(config.CARD_SAVE_DIR,
                                     get_tier_name(card.tier))
            # Create tier directory if it doesn't exists
            if not os.path.exists(tier_path):
                os.makedirs(tier_path)

            card_file_name = card.get_card_file_name()
            cardpath = os.path.join(tier_path, card_file_name)

            picturepath = os.path.join(
                config.PICTURE_SOURCE_DIR,
                card.picture_path) if card.picture_path else None
            print(f'Generating {card_file_name}')
            generate_card(card.tier, card.name, card.description, card.flavour,
                          picturepath, cardpath)

    def generate_grid(self):
        pass