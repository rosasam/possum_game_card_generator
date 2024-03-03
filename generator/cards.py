import os
import textwrap
from PIL import Image, ImageFont

from utils import config
from generator.word import encode_words, text_wrap
from utils.align import get_description_blocks_y_position

def add_layer(image, layer, card):
    if layer == 'bottom':
        filename = 'card_template_bot.png'
    elif layer == 'top':
        filename = f"card_template_top_{card.type}{'' if card.cost > 0 else '_base'}.png"
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

def add_icon(image, type):
    filename = f'{type}-large.png'
    filepath = os.path.join(config.ICONS_DIR, filename)
    layerImage = Image.open(filepath).convert('RGBA').resize((config.ICON_LARGE_SIZE_PIXELS, config.ICON_LARGE_SIZE_PIXELS))

    image.paste(layerImage, (config.CARD_TYPE_ICON_X, config.CARD_TYPE_ICON_Y), layerImage)

# Deprecated
def add_nuts(image, nuts: int):
    if nuts < 1:
        return
    filename = f'card_template_NUT.png'
    filepath = os.path.join(config.TEMPLATES_DIR, filename)
    layerImage = Image.open(filepath).convert('RGBA').resize((config.CARD_WIDTH_PIXELS, config.CARD_HEIGHT_PIXELS))

    for i in range(nuts):
        offset = (nuts - 1) * config.NUT_SPACING // 2
        x = config.NUT_SPACING * (nuts - i - 1) - offset
        image.paste(layerImage, (x, 0), layerImage)

def write_nut_cost(image, d, cost: int):
    if cost < 1:
        return
    fontsize = config.COST_FONT_SIZE
    font = ImageFont.truetype(os.path.join('fonts', config.COST_FONT_FILE), fontsize)
    text = str(cost)
    cost_width, cost_height = font.getsize(text)
    d.text((config.COST_X_POSITION - (cost_width // 2),
            config.COST_Y_POSITION - cost_height // 2),
           text,
           fill='black',
           font=font) 

def write_title(d, text):
    text = text.upper()
    fontsize = config.TITLE_FONTSIZE
    font = ImageFont.truetype(os.path.join('fonts', config.TITLE_FONT_FILE), fontsize)
    name_width, name_height = font.getsize(text)
    while name_width > config.CARD_WIDTH_PIXELS - config.TITLE_MARGIN * 2:
        fontsize -= 2
        font = ImageFont.truetype(os.path.join('fonts', config.TITLE_FONT_FILE),
                                  fontsize)
        name_width, name_height = font.getsize(text)
    d.text(((config.CARD_WIDTH_PIXELS - name_width) // 2,
            config.TITLE_Y_POSITION - name_height // 2),
           text,
           fill='black',
           font=font)

def write_description(d, text):
    words = encode_words(text.split(' '), config.KEYWORDS, config.DESCRIPTION_FONTSIZE)
    blocks = text_wrap(words, config.CARD_WIDTH_PIXELS - config.TEXT_MARGIN * 2)
    block_start_positions = get_description_blocks_y_position(blocks)

    y_position = 0

    for block, block_y_position in zip(blocks, block_start_positions):
        y_position = block_y_position
        for line in block:
            linewidth = sum([w.length for w in line])
            # This horizontally centers the text
            x_position = int(config.CARD_WIDTH_PIXELS / 2 - linewidth / 2)
            for word in line:
                d.text((x_position, y_position), word.text, fill='black', font=word.font)
                x_position += word.length
            y_position += config.DESCRIPTION_LINE_HEIGHT
        
    return y_position

def write_card_type(d, card):
    type = card.type.upper()
    base = card.cost < 0
    if card.type == 'event':
        return
    font = ImageFont.truetype(os.path.join('fonts', config.CARD_TYPE_TEXT_FONT), config.CARD_TYPE_TEXT_FONT_SIZE)
    width, _ = font.getsize(type)
    x_pos = config.CARD_TYPE_TEXT_X_POSITION - (width // 2)
    d.text((x_pos, config.CARD_TYPE_TEXT_Y_POSITION), type, fill='black', font=font)


def draw_horizontal_line(d, y_position, width, color="#dcc9b0"):
    x_start = (config.CARD_WIDTH_PIXELS - width) // 2 if width < config.CARD_WIDTH_PIXELS else config.CARD_WIDTH_PIXELS
    x_end = config.CARD_WIDTH_PIXELS - x_start
    shape = [(x_start, y_position), (x_end, y_position)]
    d.line(shape, fill =color, width = 2) 

# Deprecated
def write_lock_modifier(d, modifier: str):
    font = ImageFont.truetype(os.path.join('fonts', config.TITLE_FONT_FILE), 140)
    width, height = font.getsize(modifier)
    d.text((65 - width // 2, 95 - height // 2), modifier, fill='#4d4d4d', font=font)
