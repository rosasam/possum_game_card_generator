import sys
import os
import glob

from utils import config
from utils.google_api import get_sheets_data, download_drive_images, get_drive_image_list
from utils.file_and_path import create_pic_file_name
from generator.card_generator import Generator
from generator.card import Card
from utils.types import get_card_type

class Modes:
    test = False            # Test mode only prints one card
    single_card = False     # Prints only 1 copy of every card
    no_card_back = False    # Doesnt print cardbacks

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODES = Modes()

def set_modes(args: list[str]):
    """Gets the running modes"""
    if len(args) > 1:
        MODES.test = '--test' in args or '-t' in args
        MODES.single_card = '--single' in args or '-s' in args
        MODES.no_card_back = '--no-cardback' in args or '-nc' in args


def try_create_dir(dir_name: str) -> str:
    """Tries to create a new directory"""
    abs_path_to_new_dir = os.path.join(ROOT_DIR, dir_name)
    try:
        os.makedirs(abs_path_to_new_dir)  # Throws OSError if it exists
    except OSError:
        pass

    return abs_path_to_new_dir


def delete_old_cards(path_to_card_dir: str) -> None:
    """Delete all png, jpg, and pdf files in the given directory"""
    print('Deleting old cards...')
    for name, _, _ in os.walk(path_to_card_dir):
        old_png_files = glob.glob(os.path.join(name, '*.png'))
        old_jpg_files = glob.glob(os.path.join(name, '*.jpg'))
        old_pdf_files = glob.glob(os.path.join(name, '*.pdf'))
        old_files = old_png_files + old_jpg_files + old_pdf_files
        for file in old_files:
            os.remove(file)


def create_cards(data) -> list[Card]:
    """Create a list of all cards"""
    cards = []
    for file, row in data.iterrows():
        # Change these keys to match the keys in the csv
        field_names = config.GOOGLE_SHEETS_FIELD_NAMES
        name = row[field_names['name']]
        cost = int(row[field_names['cost']])
        cardType = row[field_names['type']]
        amount = int(row[field_names['amount']])
        picture_file_name = create_pic_file_name(name)
        description = row[field_names['description']]
        flavour = row[field_names['flavour']]

        cardType = get_card_type(cardType)
        # Dont generate card if either name or amount is undefined
        if not name and amount:
            print(
                f'\033[93mWARNING\033[0m: CSV row {file} missing name or amount'
            )
            continue

        amount = 1 if MODES.single_card else amount
        cards.append(Card(name, cost, cardType, amount, picture_file_name, description, flavour))
    return cards


def download_needed_images(data, path_to_src_pics):
    """Download all required and missing images"""
    # Only download images that are not already downloaded (based on image urls in spreadsheet)
    downloaded_images_full_path = glob.glob(os.path.join(path_to_src_pics, '*.jpg'))
    downloaded_images = [os.path.basename(d) for d in downloaded_images_full_path]

    # Images added to the spreadsheet
    needed_card_images = [f"{name.lower().replace(' ', '_')}.jpg" for name in data[config.GOOGLE_SHEETS_FIELD_NAMES['name']]]
    needed_card_images.append('card_back.jpg')

    drive_images = get_drive_image_list()
    missing_images = list(filter(
        lambda image: image['name'] not in downloaded_images and image['name'] in needed_card_images, 
        drive_images
    ))

    download_drive_images(missing_images)


def main(args: list[str]):
    set_modes(args)
    # Get data from Google Drive if set in config. Otherwise, get data from a csv provided
    data = get_sheets_data()
    generator = Generator({ "testmode": MODES.test, "no_cardback_mode": MODES.no_card_back })

    abs_path_to_card_save_dir = try_create_dir(config.CARD_SAVE_DIR)
    delete_old_cards(abs_path_to_card_save_dir)

    abs_path_to_picture_source_dir = try_create_dir(config.PICTURE_SOURCE_DIR)
    download_needed_images(data, abs_path_to_picture_source_dir)

    # Parse card data and create cards
    for card in create_cards(data):
        generator.add_card(card)
        if MODES.test:
            break

    # Generate output files
    generator.generate_cards()
    if config.GENERATE_GRID:
        print('Generating grid')
        generator.generate_grid_pdf()


if __name__ == '__main__':
    main(sys.argv)
