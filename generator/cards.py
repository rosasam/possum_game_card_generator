import os
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from utils import config


def add_layer(image, layer, type):
    if layer == 'bottom':
        filename = 'card_template_bot.png'
    elif layer == 'top':
        filename = f'card_template_top_{type}.png'
    layerImage = Image.open(os.path.join(config.TEMPLATES_DIR,
                                         filename)).convert('RGBA').resize(
                                             (config.CARD_WIDTH_PIXELS,
                                              config.CARD_HEIGHT_PIXELS))
    image.paste(layerImage, (0, 0), layerImage)


def add_picture(img, path):
    picture = Image.new('RGBA', (config.PIC_WIDTH, config.PIC_HEIGHT),
                        color='red')
    picture = Image.open(path).convert('RGBA').resize(
        (config.PIC_WIDTH, config.PIC_HEIGHT))
    width, height = picture.size

    left = (width - config.PIC_WIDTH) // 2
    top = (height - config.PIC_HEIGHT) // 2
    right = (width + config.PIC_WIDTH) // 2
    bottom = (height + config.PIC_HEIGHT) // 2

    # Crop the center of the image
    picture = picture.crop((left, top, right, bottom))

    img.paste(picture, ((config.CARD_WIDTH_PIXELS - config.PIC_WIDTH) // 2,
                        config.PIC_Y_POSITION), picture)


def write_title(d, text):
    text = text.upper()
    fontsize = config.TITLE_FONTSIZE
    font = ImageFont.truetype(os.path.join('fonts', config.TITLE_FONT_FILE), fontsize)
    name_width, name_height = font.getsize(text)
    while name_width > config.CARD_WIDTH_PIXELS - config.TEXT_LEFT_MARGIN:
        fontsize -= 10
        font = ImageFont.truetype('fonts/JustAnotherHand-Regular.ttf',
                                  fontsize)
        name_width, name_height = font.getsize(text)
    d.text(((config.CARD_WIDTH_PIXELS - name_width) // 2,
            config.TITLE_Y_POSITION + (50 - name_height) // 2),
           text,
           fill='black',
           font=font)


def write_description(d, text):
    fontsize = config.DESCRIPTION_FONTSIZE
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
                font = ImageFont.truetype('fonts/RobotoCondensed-Bold.ttf',
                                          fontsize)
            else:
                font = ImageFont.truetype('fonts/RobotoCondensed-Regular.ttf',
                                          fontsize)

            width, height = font.getsize(word)
            heights.append(height)
            d.text((x_word, y_text), word, fill='black', font=font)

            # Don't add whitespace if next character is a punctuation mark
            if i + 1 < len(words) and words[i + 1] in ['.', ',']:
                x_word += width
            else:
                x_word += width + 8
        y_text += max(heights)
    return y_text


def write_flavour(d, text, start_height):
    fontsize = config.DESCRIPTION_FONTSIZE
    font = ImageFont.truetype('fonts/RobotoCondensed-Italic.ttf', fontsize)

    lines = textwrap.wrap(text, width=config.CHARACTERS_PER_ROW + 4)
    y_text = config.FLAVOUR_START_HEIGHT if config.FLAVOUR_START_HEIGHT > start_height + \
        60 else start_height + 60
    for line in lines:
        width, height = font.getsize(line)
        d.text((config.TEXT_LEFT_MARGIN, y_text), line, fill='black', font=font)
        y_text += height


def write_nut_cost(card_image, d, cost):
    if not cost: # Dont draw 0 cost
        return
    cost = str(cost)
    fontsize = 120
    text_font = ImageFont.truetype('fonts/JustAnotherHand-Regular.ttf', fontsize)
    text_width, text_height = text_font.getsize(cost)
    text_position = ((config.CARD_WIDTH_PIXELS - text_width) // 2, 
        config.COST_POSITION_Y + (50 - text_height) // 2)

    drop_shadow_font = ImageFont.truetype('fonts/JustAnotherHand-Regular.ttf', fontsize + 20)
    drop_shadow_width, drop_shadow_height = drop_shadow_font.getsize(cost)
    drop_shadow_position = ((config.CARD_WIDTH_PIXELS - drop_shadow_width) // 2, 
        config.COST_POSITION_Y + (50 - drop_shadow_height) // 2)
    drop_shadow_image = Image.new('RGBA', (config.CARD_WIDTH_PIXELS, config.CARD_HEIGHT_PIXELS))
    drop_shadow_draw = ImageDraw.Draw(drop_shadow_image)
    drop_shadow_draw.text(xy=drop_shadow_position, text=cost, fill='black', font=drop_shadow_font)
    drop_shadow_image = drop_shadow_image.filter(ImageFilter.BoxBlur(3))
    card_image.paste(drop_shadow_image, drop_shadow_image)

    d.text(text_position, cost, fill='white', font=text_font)