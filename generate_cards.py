import sys
import os
import glob

from utils import config
from utils.google_api import get_sheets_data, download_drive_images
from generator.card_generator import Generator
from generator.card import Card
from utils.types import get_card_type


def main(args):
    # Get data from Google Drive if set in config. Otherwise, get data from a csv provided
    data = get_sheets_data()
    # Test mode only prints one card
    testmode = False
    single_card_mode = False
    no_cardback_mode = False
    if len(args) > 1:
        testmode = '--test' in args or '-t' in args
        single_card_mode = '--single' in args or '-s' in args
        no_cardback_mode = '--no-cardback' in args or '-nc' in args
    generator = Generator({ "testmode": testmode, "no_cardback_mode": no_cardback_mode })

    abs_path_to_this_dir = os.path.dirname(os.path.abspath(__file__))

    # Create output dir
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
    download_drive_images(data)

    # Parse card data and create cards
    for file, row in data.iterrows():
        # Change these keys to match the keys in the csv
        field_names = config.GOOGLE_SHEETS_FIELD_NAMES
        name = row[field_names['name']]
        cost = int(row[field_names['cost']])
        cardType = row[field_names['type']]
        amount = int(row[field_names['amount']])
        picture_file_name = f"{name.lower().replace(' ', '_')}.jpg"  # Same logic as in card.py
        description = row[field_names['description']]
        flavour = row[field_names['flavour']]

        cardType = get_card_type(cardType)
        # Dont generate card if either name or amount is undefined
        if not name and amount:
            print(
                f'\033[93mWARNING\033[0m: CSV row {file} missing name or amount'
            )
            continue

        amount = 1 if single_card_mode else amount
        generator.add_card(
            Card(name, cost, cardType, amount, picture_file_name, description,
                 flavour))
        if testmode:
            break

    # Generate output files
    generator.generate_cards()
    if config.GENERATE_GRID:
        print('Generating grid')
        generator.generate_grid_pdf()


if __name__ == '__main__':
    main(sys.argv)
