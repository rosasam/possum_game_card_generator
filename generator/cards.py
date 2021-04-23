import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

from utils import config
from utils.tiers import get_tier_name


# Generates and saves a single card
def generate_card(tier, name, description, flavour, picturepath, filename):
    card = Image.new('RGBA', (config.WIDTH, config.HEIGHT))

    add_background(card, 'bottom', tier)
    if picturepath:
        try:
            add_picture(card, picturepath)
        except Exception as e:
            print('--- WARNING ---')
            print(f'Picture file for {name} could not be found.')
            print(f'Tried path: "{picturepath}"')
            print('---------------')
    add_background(card, 'top', tier)

    d = ImageDraw.Draw(card)
    write_title(d, name, tier)

    if description:
        description_bottom_y = write_description(
            d, description, tier)
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
    background = Image.open(os.path.join(config.TEMPLATES_DIR, filename))
    assert background.size == (700, 1000)
    image.paste(background, (0, 0), background)


def add_picture(img, path):
    picture = Image.new(
        'RGBA', (config.PIC_WIDTH, config.PIC_HEIGHT), color='red')
    picture = Image.open(path).convert('RGBA')
    width, height = picture.size

    left = (width - config.PIC_WIDTH)//2
    top = (height - config.PIC_HEIGHT)//2
    right = (width + config.PIC_WIDTH)//2
    bottom = (height + config.PIC_HEIGHT)//2

    # Crop the center of the image
    picture = picture.crop((left, top, right, bottom))

    img.paste(picture, ((config.WIDTH - config.PIC_WIDTH) //
              2, config.PIC_Y_POSITION), picture)


def write_title(d, text, tier):
    text = text.upper()
    fontsize = config.TITLE_FONTSIZE
    color = 'white' if tier == 4 else 'black'
    font = ImageFont.truetype('fonts/JustAnotherHand-Regular.ttf', fontsize)
    name_width, name_height = font.getsize(text)
    while name_width > config.WIDTH - config.TEXT_LEFT_MARGIN:
        fontsize -= 10
        font = ImageFont.truetype(
            'fonts/JustAnotherHand-Regular.ttf', fontsize)
        name_width, name_height = font.getsize(text)
    d.text(
        ((config.WIDTH-name_width)//2, config.TITLE_Y_POSITION + (50-name_height)//2),
        text,
        fill=color,
        font=font)


def write_description(d, text, tier):
    # DISCLAIMER:
    # Keyword koden kommer att få dina ögon o blöda.
    fontsize = config.DESCRIPTION_FONTSIZE
    color = 'white' if tier == 4 else 'black'
    lines = textwrap.wrap(text, width=config.CHARACTERS_PER_ROW)
    y_text = config.DESCRIPTION_Y_POSITION
    for line in lines:
        words = line.replace(',', ' ,').replace('.', ' .').split(' ')
        heights = []
        x_word = config.TEXT_LEFT_MARGIN

        # Write text word by word to allow keyword highlighting
        for i, word in enumerate(words):
            if word.lower() in config.KEYWORDS:
                word = word if word.isupper() else word.capitalize()
                font = ImageFont.truetype(
                    'fonts/RobotoCondensed-Bold.ttf', fontsize)
            else:
                font = ImageFont.truetype(
                    'fonts/RobotoCondensed-Regular.ttf', fontsize)

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
    fontsize = config.DESCRIPTION_FONTSIZE
    color = 'white' if tier == 4 else 'black'
    font = ImageFont.truetype('fonts/RobotoCondensed-Italic.ttf', fontsize)

    lines = textwrap.wrap(text, width=config.CHARACTERS_PER_ROW+4)
    y_text = config.FLAVOUR_START_HEIGHT if config.FLAVOUR_START_HEIGHT > start_height + \
        60 else start_height + 60
    for line in lines:
        width, height = font.getsize(line)
        d.text(
            (config.TEXT_LEFT_MARGIN, y_text),
            line,
            fill=color,
            font=font)
        y_text += height
