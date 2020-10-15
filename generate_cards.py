from PIL import Image, ImageDraw, ImageFont
import textwrap
import pandas as pd
import sys, os
import glob
import math

# Card size in pixels
WIDTH = 700
HEIGHT = 1000

# Picture size
PIC_WIDTH = 660
PIC_HEIGHT = 550
PIC_Y_POSITION = 20

# Text
TEXT_LEFT_MARGIN = 50
TITLE_FONTSIZE = 60
TITLE_Y_POSITION = PIC_Y_POSITION + PIC_HEIGHT + 12
DESCRIPTION_FONTSIZE = 35
CHARACTERS_PER_ROW = 42
DESCRIPTION_Y_POSITION = TITLE_Y_POSITION + 100
FLAVOUR_START_HEIGHT = HEIGHT - 300

# Directories
CARD_SAVE_DIR = 'generated_cards'
PICTURE_SOURCE_DIR = 'source_pictures'
TEMPLATES_DIR = 'templates'
KEYWORDS_FILE = 'keywords.txt'

# Globals for grid generation
GENERATE_GRID = True
MAX_GRID_WIDTH = 10
MAX_GRID_HEIGHT = 7
MAX_CARDS = MAX_GRID_WIDTH * MAX_GRID_HEIGHT

def main(args):
    if len(args) < 2:
        print('Please provide filename for the csv.')
        exit()

    filename = args[1]
    print(f'generating cards from csv:{filename}.')
    data = pd.read_csv(filename,keep_default_na=False,na_values=['NaN'])
    skipped = []
    generated = 0

    # Read keyword file
    if os.path.exists(KEYWORDS_FILE):
        print('Keyword file found.')
        with open(KEYWORDS_FILE, 'r') as f:
           keywords = [line.strip().lower() for line in f.readlines()]
    else:
        print('––– No keyword file found –––')
        keywords = []

    # Create directories for each tier
    if not os.path.exists(CARD_SAVE_DIR):
        os.makedirs(CARD_SAVE_DIR)
    else:
        print('Deleting old cards...')
        for name, _, _ in os.walk(CARD_SAVE_DIR):
            images = glob.glob(os.path.join(name, '*.png'))
            for i in images:
                os.remove(i)

    if not os.path.exists(PICTURE_SOURCE_DIR):
        os.makedirs(PICTURE_SOURCE_DIR)

    for i, row in data.iterrows():
        # Change these keys to match the keys in the csv
        amount = row['Amount']
        tier = row['Tier']
        name = row['Name']
        description = row['Effect']
        flavour = row['Card text']
        picture = row['Picture']

        if amount and name:
            amount = int(amount)
            tier = int(tier) if tier else ''
            # Create tier directory if it doesn't exists
            tier_path = os.path.join(CARD_SAVE_DIR, get_tier_name(tier))
            if not os.path.exists(tier_path):
                os.makedirs(tier_path)
            # Generate 'amount' many cards
            for i in range(1, amount + 1):
                cardname = f"{get_tier_name(tier)}_{name.lower().replace(' ', '_')}_{i}"
                cardpath = os.path.join(tier_path, cardname)
                picturepath = os.path.join(PICTURE_SOURCE_DIR, picture) if picture else None
                print(f'Generating {cardname}')
                generate_card(
                    tier, name, description, flavour, picturepath, cardpath, keywords
                )
            generated += 1
        else:
            print('--- WARNING ---')
            print(f'Invalid csv row ({i}): Amount and name must be set for all rows!')
            print('---------------')
            skipped.append(row)

    print(f'Generated {generated} unique cards (duplicates not counted).')
    print(f'Skipped {len(skipped)} rows:')
    for row in skipped:
        print(row)

    if GENERATE_GRID:
        print('Generating grid')
        generate_grid()


# Generates and saves a single card
def generate_card(tier, name, description, flavour, picturepath, filename, keywords):
    card = Image.new('RGBA', (WIDTH, HEIGHT))
    
    add_background(card, 'bottom', tier)
    if picturepath:
        try:
            add_picture(card, picturepath)
        except FileNotFoundError as e:
            print('--- WARNING ---')
            print(f'Picture file for {name} could not be found.')
            print(f'Tried path: "{picturepath}"')
            print('---------------')
    add_background(card, 'top', tier)
    
    d = ImageDraw.Draw(card)
    write_title(d, name, tier)

    if description:
        description_bottom_y = write_description(d, description, tier, keywords)
    else:
        description_bottom_y = 0
    if flavour:
        write_flavour(d, flavour, description_bottom_y, tier)

    card.save(f'{filename}.png')


def add_background(image, layer, tier):
    if layer == 'bottom':
        filename = 'card_template_bot.png'
    elif layer == 'top':
        tier_name = get_tier_name(tier)
        filename = f'card_template_top_{tier_name}.png'
    background = Image.open(os.path.join(TEMPLATES_DIR, filename))
    assert background.size == (700, 1000)
    image.paste(background, (0, 0), background)

def add_picture(img, path):
    picture = Image.new('RGBA', (PIC_WIDTH, PIC_HEIGHT), color='red')
    picture = Image.open(path).convert('RGBA')
    width, height = picture.size

    left = (width - PIC_WIDTH)//2
    top = (height - PIC_HEIGHT)//2
    right = (width + PIC_WIDTH)//2
    bottom = (height + PIC_HEIGHT)//2

    # Crop the center of the image
    picture = picture.crop((left, top, right, bottom))

    img.paste(picture, ((WIDTH - PIC_WIDTH) // 2, PIC_Y_POSITION), picture)

def write_title(d, text, tier):
    text = text.upper()
    fontsize = TITLE_FONTSIZE
    color = 'white' if tier == 4 else 'black'
    font = ImageFont.truetype('fonts/JustAnotherHand-Regular.ttf', fontsize)
    name_width, name_height = font.getsize(text)
    while name_width > WIDTH - TEXT_LEFT_MARGIN:
        fontsize -= 10
        font = ImageFont.truetype('fonts/JustAnotherHand-Regular.ttf', fontsize)
        name_width, name_height = font.getsize(text)
    d.text(
        ((WIDTH-name_width)//2, TITLE_Y_POSITION + (50-name_height)//2), 
        text, 
        fill=color,
        font=font)

def write_description(d, text, tier, keywords):
    # DISCLAIMER:
    # Keyword koden kommer att få dina ögon o blöda. 
    fontsize = DESCRIPTION_FONTSIZE
    color = 'white' if tier == 4 else 'black'
    lines = textwrap.wrap(text, width=CHARACTERS_PER_ROW)
    y_text = DESCRIPTION_Y_POSITION
    for line in lines:
        words = line.replace(',', ' ,').replace('.', ' .').split(' ')
        heights = []
        x_word = TEXT_LEFT_MARGIN

        # Write text word by word to allow keyword highlighting
        for i, word in enumerate(words):
            if word.lower() in keywords:
                word = word if word.isupper() else word.capitalize()
                font = ImageFont.truetype('fonts/RobotoCondensed-Bold.ttf', fontsize)
            else:
                font = ImageFont.truetype('fonts/RobotoCondensed-Regular.ttf', fontsize)
        
            width, height = font.getsize(word)
            heights.append(height)
            d.text(
                (x_word, y_text), 
                word,
                fill=color,
                font=font)
            
            # Don't add whitespace if next character is a punctuation mark
            if i + 1 < len(words) and words[i + 1] in ['.', ',']:
                x_word += width
            else:
                x_word += width + 8
        y_text += max(heights)
    return y_text

def write_flavour(d, text, start_height, tier):
    fontsize = DESCRIPTION_FONTSIZE
    color = 'white' if tier == 4 else 'black'
    font = ImageFont.truetype('fonts/RobotoCondensed-Italic.ttf', fontsize)
    
    lines = textwrap.wrap(text, width=CHARACTERS_PER_ROW+4)
    y_text = FLAVOUR_START_HEIGHT if FLAVOUR_START_HEIGHT > start_height + 60 else start_height + 60 
    for line in lines:
        width, height = font.getsize(line)
        d.text(
            (TEXT_LEFT_MARGIN, y_text),
            line,
            fill=color,
            font=font)
        y_text += height

def get_color(tier):
    # 0: starter
    # 1: common (beige)
    # 2: rare (blue)
    # 3: epic (purple)
    # 4: legendary (gold)
    if tier == 0:
        return (194, 223, 227)
    elif tier == 1:
        return (242, 204, 143)
    elif tier == 2:
        return (76, 201, 240)
    elif tier == 3:
        return (240, 80, 174)
    elif tier == 4:
        return (253, 241, 72)
    elif tier == 10:
        return 'white'
    else:
        return (150, 150, 150)

def get_tier_name(tier):
    if tier == 0:
        return 'base'
    elif tier == 1:
        return 'common'
    elif tier == 2:
        return 'rare'
    elif tier == 3:
        return 'epic'
    elif tier == 4:
        return 'legendary'
    elif tier == 10:
        return 'EGG'
    else:
        return 'unknown'

# ---------------
# GRID GENERATION
# ---------------
def generate_grid():
    tiers = filter(lambda d: '.' not in d, os.listdir(CARD_SAVE_DIR))
    for tier in tiers:
        cards = sorted(glob.glob(os.path.join(CARD_SAVE_DIR, tier, '*.png')))
        print(f'Generating grid for TIER: {tier.upper()}')
        # Process batches of 70
        for i in range(math.ceil(len(cards) / MAX_CARDS)):
            j = (i+1)*MAX_CARDS if (i+1)*MAX_CARDS < len(cards) else len(cards)
            card_grid, grid_size = combine_cards(cards[i*MAX_CARDS:j])
            name = f'{tier}_{i+1}_{grid_size[0]//WIDTH}x{grid_size[1]//HEIGHT}_{len(cards)}.png'
            print(f'Saving {name}')
            card_grid.save(os.path.join(CARD_SAVE_DIR, name))
   

def combine_cards(cards):
    images = [Image.open(c) for c in cards]

    # Calculate final grid size
    nof_rows = math.ceil(len(images) / MAX_GRID_WIDTH)
    if len(images) > MAX_GRID_WIDTH:
        grid_size = (MAX_GRID_WIDTH * WIDTH, nof_rows * HEIGHT)
    else:
        # Add an extra row to grids with only one row, required by Tabletop Simulator
        grid_size = (WIDTH * len(images), HEIGHT * 2)
    card_grid = Image.new('RGBA', grid_size)

    # Process batches of MAX_GRID_WIDTH
    for i in range(nof_rows):
        j = (i+1)*MAX_GRID_WIDTH if (i+1)*MAX_GRID_WIDTH < len(images) else len(images)
        row = combine_rows(images[i*MAX_GRID_WIDTH:j])
        row_height = row.size[1]
        card_grid.paste(row, (0, i * row_height))

    return card_grid, grid_size


def combine_rows(images):
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    card_row = Image.new('RGBA', (total_width, max_height))

    x_offset = 0
    for im in images:
        card_row.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return card_row


if __name__ == '__main__':
    main(sys.argv)