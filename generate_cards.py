import sys
import os
import glob
import pandas as pd

from utils import config
from utils.tiers import get_tier_name
from generator.cards import generate_card
from generator.grid import generate_grid


def main(args):
    if len(args) < 2:
        print('Please provide filename for the csv.')
        exit()

    filename = args[1]
    print(f'generating cards from csv:{filename}.')
    data = pd.read_csv(filename, keep_default_na=False, na_values=['NaN'])
    skipped = []
    generated = 0

    keywords = config.KEYWORDS

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

    for i, row in data.iterrows():
        # Change these keys to match the keys in the csv
        field_names = config.GOOGLE_SHEETS_FIELD_NAMES
        amount = row[field_names['amount']]
        tier = row[field_names['tier']]
        name = row[field_names['name']]
        description = row[field_names['description']]
        flavour = row[field_names['flavour']]
        picture = row[field_names['picture']]

        if amount and name:
            amount = int(amount)
            tier = int(tier) if tier else ''
            # Create tier directory if it doesn't exists
            tier_path = os.path.join(config.CARD_SAVE_DIR, get_tier_name(tier))
            if not os.path.exists(tier_path):
                os.makedirs(tier_path)
            # Generate 'amount' many cards
            for i in range(1, amount + 1):
                # Windows filenames can't contains some special characters.
                cardname = f"{get_tier_name(tier)}_{name.lower().replace(' ', '_')}_{i}"
                for c in config.FORBIDDEN_CHARACTERS:
                    cardname = cardname.replace(c, '')
                cardpath = os.path.join(tier_path, cardname)
                picturepath = os.path.join(
                    config.PICTURE_SOURCE_DIR, picture) if picture else None
                print(f'Generating {cardname}')
                generate_card(
                    tier, name, description, flavour, picturepath, cardpath, keywords
                )
            generated += 1
        else:
            print('--- WARNING ---')
            print(
                f'Invalid csv row ({i}): Amount and name must be set for all rows!')
            print('---------------')
            skipped.append(row)

    print(f'Generated {generated} unique cards (duplicates not counted).')
    print(f'Skipped {len(skipped)} rows:')
    for row in skipped:
        print(row)

    if config.GENERATE_GRID:
        print('Generating grid')
        generate_grid()


if __name__ == '__main__':
    main(sys.argv)
