import sys
import os
import glob
import pandas as pd

from utils import config
from utils.tiers import get_tier_name
from utils.google_api import get_sheets_data, download_drive_images
from generator.card_generator import Generator
from generator.cards import generate_card
from generator.grid import generate_grid
from generator.card import Card


def main(args):
    if not config.USE_GOOGLE_API:
        if len(args) < 2:
            print(
                'Please provide card csv or enable Google API in config. Exiting...'
            )
            exit()
        filename = args[1]
        print(f'generating cards from csv:{filename}.')
        data = pd.read_csv(filename, keep_default_na=False, na_values=['NaN'])
    else:
        data = get_sheets_data()

    generator = Generator()

    # Create directories for each tier
    if not os.path.exists(config.CARD_SAVE_DIR):
        os.makedirs(config.CARD_SAVE_DIR)
    else:
        print('Deleting old cards...')
        for name, _, _ in os.walk(config.CARD_SAVE_DIR):
            images = glob.glob(os.path.join(name, '*.png'))
            for i in images:
                os.remove(i)

    if not os.path.exists(config.PICTURE_SOURCE_DIR):
        os.makedirs(config.PICTURE_SOURCE_DIR)

    if config.USE_GOOGLE_API:
        download_drive_images(data)

    for i, row in data.iterrows():
        # Change these keys to match the keys in the csv
        field_names = config.GOOGLE_SHEETS_FIELD_NAMES
        name = str(row[field_names['name']])
        tier = int(row[field_names['tier']])
        amount = int(row[field_names['amount']])
        picture = row[field_names['picture']]
        description = str(row[field_names['description']])
        flavour = str(row[field_names['flavour']])

        if amount and name:
            generator.add_card(
                Card(name, tier, amount, picture, description, flavour))
        else:
            print(
                f'\033[93mWARNING\033[0m: CSV row {i} missing name or amount')
    generator.generate_cards()

    if config.GENERATE_GRID:
        print('Generating grid')
        generate_grid()


if __name__ == '__main__':
    main(sys.argv)
