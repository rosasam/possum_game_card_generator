import os

from PIL import Image, ImageFont, ImageDraw
from generator.description_block import create_blocks
from generator.word import cap_text_to_max_height, write_text

from utils import config
from utils.align import get_description_blocks_y_position


def add_template(image, card):
    filename = (
        f"card_template_top_{card.type}{'' if card.cost > 0 else '_base'}.png"
    )

    layer_image = (
        Image.open(os.path.join(config.TEMPLATES_DIR, filename))
        .convert("RGBA")
        .resize((config.CARD_WIDTH_PIXELS, config.CARD_HEIGHT_PIXELS))
    )
    image.paste(layer_image, (0, 0), layer_image)


def add_picture(img, path, pic_width=config.PIC_WIDTH, pic_height=config.PIC_HEIGHT):
    picture = Image.new("RGBA", (pic_width, pic_height), color="red")
    picture = Image.open(path).convert("RGBA").resize((pic_width, pic_height))
    width, height = picture.size

    left = (width - pic_width) // 2
    top = (height - pic_height) // 2
    right = (width + pic_width) // 2
    bottom = (height + pic_height) // 2

    # Crop the center of the image
    picture = picture.crop((left, top, right, bottom))

    img.paste(
        picture,
        ((config.CARD_WIDTH_PIXELS - pic_width) // 2, config.PIC_Y_POSITION),
        picture,
    )


def add_description_picture(
    img: Image, path: str, pic_width:int=config.PIC_WIDTH, pic_height:int=config.PIC_HEIGHT
):
    picture = Image.open(path).convert("RGBA").resize((pic_width, pic_height))
    img.paste(
        picture,
        (0, 0),
        picture,
    )


def add_card_type_icon(image, type):
    filename = f"{type}-large.png"
    filepath = os.path.join(config.ICONS_DIR, filename)
    layerImage = (
        Image.open(filepath)
        .convert("RGBA")
        .resize((config.CARD_TYPE_ICON_SIZE_PIXELS, config.CARD_TYPE_ICON_SIZE_PIXELS))
    )

    image.paste(
        layerImage, (config.CARD_TYPE_ICON_X, config.CARD_TYPE_ICON_Y), layerImage
    )


def write_nut_cost(d, cost: int):
    if cost < 1 or cost == 10:
        return
    fontsize = config.COST_FONT_SIZE
    font = ImageFont.truetype(os.path.join("fonts", config.COST_FONT_FILE), fontsize)
    text = str(cost)
    d.text(
        (config.COST_X_POSITION, config.COST_Y_POSITION),
        text,
        fill="black",
        font=font,
        anchor='mm',
    )


def write_title(d, text):
    text = text.upper()
    fontsize = config.TITLE_FONTSIZE
    font = ImageFont.truetype(os.path.join("fonts", config.TITLE_FONT_FILE), fontsize)
    while font.getlength(text) > config.CARD_WIDTH_PIXELS - config.TITLE_MARGIN * 2:
        fontsize -= 2
        font = ImageFont.truetype(
            os.path.join("fonts", config.TITLE_FONT_FILE), fontsize
        )
    d.text(
        (
            config.CARD_WIDTH_PIXELS // 2,
            config.TITLE_Y_POSITION,
        ),
        text,
        fill="black",
        font=font,
        anchor='mm',
    )


def write_description(image, d, text):
    blocks = create_blocks(text)
    block_start_positions = get_description_blocks_y_position(blocks)

    for block, block_y_position in zip(blocks, block_start_positions):
        block.render(image, d, block_y_position)
    return (
        block_start_positions[-1] + blocks[-1].height
        if len(blocks) > 0
        else config.DESCRIPTION_Y_POSITION
    )


def write_card_type(d, card):
    if card.type == "event":
        return
    
    font = ImageFont.truetype(
        os.path.join("fonts", config.CARD_TYPE_TEXT_FONT),
        config.CARD_TYPE_TEXT_FONT_SIZE,
    )
    x_pos = config.CARD_TYPE_TEXT_X_POSITION
    y_pos = config.CARD_TYPE_TEXT_Y_POSITION
    d.text(
        (x_pos, y_pos),
        card.type.upper(),
        fill="black",
        font=font,
        anchor='mm',
    )


def write_event_title(img, name: str):
    rotated_img = Image.new(
        "RGBA", (config.CARD_HEIGHT_PIXELS, config.CARD_WIDTH_PIXELS), (0, 0, 0, 0)
    )
    d = ImageDraw.Draw(rotated_img)
    font = ImageFont.truetype(
        os.path.join("fonts", config.TITLE_FONT_FILE), config.EVENT_TITLE_FONTSIZE
    )
    d.text(
        (
            config.CARD_HEIGHT_PIXELS // 2,
            config.EVENT_TITLE_Y,
        ),
        name,
        fill="white",
        font=font,
        stroke_width=3,
        stroke_fill="black",
        anchor='mm',
    )
    # d.rectangle((0,0, config.CARD_HEIGHT_PIXELS, config.CARD_WIDTH_PIXELS), fill=None, outline='green', width=2)
    unrotated = rotated_img.rotate(90, expand=True)
    img.paste(unrotated, None, unrotated)


def write_event_description(img, text: str):
    EVENT_DESCRIPTION_WIDTH = 600
    EVENT_DESCRIPTION_HEIGHT = 120
    rotated_img = Image.new(
        "RGBA", (config.CARD_HEIGHT_PIXELS, config.CARD_WIDTH_PIXELS), (0, 0, 0, 0)
    )
    d = ImageDraw.Draw(rotated_img)
    paragraphs, line_height = cap_text_to_max_height(
        text, EVENT_DESCRIPTION_HEIGHT, EVENT_DESCRIPTION_WIDTH
    )
    write_text(
        d,
        paragraphs,
        (config.CARD_HEIGHT_PIXELS - EVENT_DESCRIPTION_WIDTH) // 2,
        config.EVENT_DESCRIPTION_Y,
        EVENT_DESCRIPTION_WIDTH,
        line_height=line_height,
    )
    unrotated = rotated_img.rotate(90, expand=True)
    img.paste(unrotated, None, unrotated)
