import sys
import os
import glob
import pandas as pd

from utils import config
from utils.google_api import get_sheets_data, download_drive_images
from generator.card_generator import Generator
from generator.card import Card


def main(args):
    # Get data from Google Drive if set in config. Otherwise, get data from a csv provided
    if config.USE_GOOGLE_API:
        data = get_sheets_data()
    else:
        if len(args) < 2:
            print(
                'Please provide card csv or enable Google API in config. Exiting...'
            )
            exit()
        filename = args[1]
        print(f'generating cards from csv:{filename}.')
        data = pd.read_csv(filename, keep_default_na=False, na_values=['NaN'])

    generator = Generator()

    # Create directories for each tier
    if not os.path.exists(config.CARD_SAVE_DIR):
        os.makedirs(config.CARD_SAVE_DIR)

    # Delete all old cards
    print('Deleting old cards...')
    for name, _, _ in os.walk(config.CARD_SAVE_DIR):
        images = glob.glob(os.path.join(name, '*.png'))
        for i in images:
            os.remove(i)

        pdfs = glob.glob(os.path.join(name, '*.pdf'))
        for pdf in pdfs:
            os.remove(pdf)

    # Create source pictures directory
    if not os.path.exists(config.PICTURE_SOURCE_DIR):
        os.makedirs(config.PICTURE_SOURCE_DIR)

    # Download source pictures
    if config.USE_GOOGLE_API:
        download_drive_images(data)

    # Fetch and parse card data
    for i, row in data.iterrows():
        # Change these keys to match the keys in the csv
        field_names = config.GOOGLE_SHEETS_FIELD_NAMES
        name = row[field_names['name']]
        tier = int(row[field_names['tier']])
        amount = int(row[field_names['amount']])
        picture_file_name = row[field_names['picture']]
        description = row[field_names['description']]
        flavour = row[field_names['flavour']]

        # Dont generate card if either name or amount is defined
        if not name and amount:
            print(
                f'\033[93mWARNING\033[0m: CSV row {i} missing name or amount')
            continue

        generator.add_card(
            Card(name, tier, amount, picture_file_name, description, flavour))

    # Generate output files
    generator.generate_cards()
    if config.GENERATE_GRID:
        print('Generating grid')
        generator.generate_grid_pdf()


if __name__ == '__main__':
    main(sys.argv)
