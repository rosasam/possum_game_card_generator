import os
from PIL import Image, ImageFont
from utils import config

from utils.align import get_description_width


def render_tags(image, d, height, tags):
    x_positions = get_tag_x_positions(tags)
    for tag_tuple, x in zip(tags, x_positions):
        tag, inner_text = tag_tuple
        render_tag(image, d, x, height, tag, inner_text)

def render_tag(image, d, x, y, tag: str, inner_text: str):
    if tag == 'nut':
        try:
            nut_amount = int(inner_text)
            for nut_x in reversed(get_nut_icons_positions(nut_amount)):
                draw_icon(image, x + nut_x, y, 'NUT')
        except Exception:
            effect_mod = inner_text
            font = get_icon_font()
            l, t, r, b = font.getbbox(inner_text)
            width = r-l
            height = b-t
            d.text((x, y + (config.ICON_LARGE_SIZE_PIXELS // 2) - height // 2), effect_mod, fill='black', font=font)
            draw_icon(image, x + width + 5, y, tag) 
        
    if tag in ['steal', 'lock']:
        effect_mod = inner_text
        font = get_icon_font()
        l, t, r, b = font.getbbox(inner_text)
        width = r-l
        height = b-t
        d.text((x, y + (config.ICON_LARGE_SIZE_PIXELS // 2) - height // 2), effect_mod, fill='black', font=font)
        draw_icon(image, x + width + 5, y, tag)


def draw_icon(image, x, y, type):
    filename = f'{type}-large.png'
    filepath = os.path.join(config.ICONS_DIR, filename)
    icon_image = Image.open(filepath).convert('RGBA').resize((config.ICON_LARGE_SIZE_PIXELS, config.ICON_LARGE_SIZE_PIXELS))
    image.paste(icon_image, (x, y), icon_image)

def get_nut_icons_width(n_nuts: int) -> int:
    return get_nut_icons_positions(n_nuts)[-1] + config.ICON_LARGE_SIZE_PIXELS

def get_nut_icons_positions(n_nuts: int):
    return [i * config.ICON_LARGE_SIZE_PIXELS - i * 44 for i in range(n_nuts)]

def get_icon_and_text_width(text) -> int:
    font = get_icon_font()
    width = font.getlength(text)
    return config.ICON_LARGE_SIZE_PIXELS + width + 5

def get_icon_font():
    return ImageFont.truetype(os.path.join('fonts', config.ICON_LARGE_FONT), config.ICON_LARGE_FONT_SIZE)

def get_tag_x_positions(tags: tuple[str, str]):
    tags = [t for t in tags if t[0] in ['nut', 'steal', 'lock']]
    icon_widths = [get_tag_width(t) for t in tags]
    icons_total_width = sum(icon_widths)
    text_area_width = get_description_width()
    normalized_widths = [w / icons_total_width for w in icon_widths]
    text_area_sections = [w * text_area_width for w in normalized_widths]
    areas_end_x = [sum(text_area_sections[0:i+1] + [config.TEXT_MARGIN]) for i in range(len(text_area_sections))]
    icons_start_x = [int(area_end_x - area_w / 2 - icon_w / 2) for area_end_x, area_w, icon_w in zip(areas_end_x, text_area_sections, icon_widths)]
    return icons_start_x

def get_tag_width(tag: tuple[str, str]):
    tag_name, text = tag
    if tag_name == 'nut':
        try:
            nut_n = int(text)
            return get_nut_icons_width(nut_n)
        except Exception:
            return get_icon_and_text_width(text)
    if tag_name in ['steal', 'lock']:
        return get_icon_and_text_width(text)
    # Trap and pouch icons get their own row
    if tag_name in ['trap', 'pouch']:
        return 0
    return 0