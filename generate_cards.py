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
    abs_path_to_this_dir = os.path.dirname(os.path.abspath(__file__))

    # Create directories for each tier
    abs_path_to_card_save_dir = os.path.join(abs_path_to_this_dir,
                                             config.CARD_SAVE_DIR)
    try:
        os.makedirs(abs_path_to_card_save_dir)  # Throws OSError if it exists
    except OSError:
        pass

    # Delete all old cards
    print('Deleting old cards...')
    for name, _, _ in os.walk(abs_path_to_card_save_dir):
        old_png_files = glob.glob(os.path.join(name, '*.png'))
        old_jpg_files = glob.glob(os.path.join(name, '*.jpg'))
        old_pdf_files = glob.glob(os.path.join(name, '*.pdf'))
        old_files = old_png_files + old_jpg_files + old_pdf_files
        for file in old_files:
            os.remove(file)

    # Create source pictures directory
    abs_path_to_picture_source_dir = os.path.join(abs_path_to_this_dir,
                                                  config.PICTURE_SOURCE_DIR)
    try:
        os.makedirs(abs_path_to_picture_source_dir)
    except OSError:
        pass

    # Download source pictures
    if config.USE_GOOGLE_API:
        download_drive_images(data)

    # Parse card data and create cards
    for file, row in data.iterrows():
        # Change these keys to match the keys in the csv
        field_names = config.GOOGLE_SHEETS_FIELD_NAMES
        name = row[field_names['name']]
        cost = int(row[field_names['cost']])
        tier = int(row[field_names['tier']])
        amount = int(row[field_names['amount']])
        picture_file_name = f"{name.lower().replace(' ', '_')}.jpg"  # Same logic as in card.py
        description = row[field_names['description']]
        flavour = row[field_names['flavour']]

        # Dont generate card if either name or amount is defined
        if not name and amount:
            print(
                f'\033[93mWARNING\033[0m: CSV row {file} missing name or amount'
            )
            continue

        generator.add_card(
            Card(name, cost, tier, amount, picture_file_name, description,
                 flavour))

    # Generate output files
    generator.generate_cards()
    if config.GENERATE_GRID:
        print('Generating grid')
        generator.generate_grid_pdf()


if __name__ == '__main__':
    main(sys.argv)
