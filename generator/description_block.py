from generator.line import draw_horizontal_line
from generator.icon import draw_icon, render_tags
from generator.word import cap_text_to_max_height, encode_text, text_wrap, write_text
from utils import config
from utils.align import get_description_width, get_paragraphs_height
import re


class DescriptionBlock:

    def __init__(self):
        raise NotImplementedError()

    def render(self, img, d, y):
        raise NotImplementedError()

    def height(self) -> int:
        raise NotImplementedError()
    
    
class TagsRowBlock(DescriptionBlock):

    def __init__(self, tags: list[list[str, str]]):
        self.tags = tags
        self.height = config.ICON_LARGE_SIZE_PIXELS + config.BLOCK_VERTICAL_PADDING * 2

    def render(self, img, d, y):
        render_tags(img, d, y, self.tags)

    def height(self):
        return self.height


class TagBlock(DescriptionBlock):

    def __init__(self, tag, max_height=config.DESCRIPTION_MAX_HEIGHT):
        self.icon = tag[0]
        self.icon_text_gap_px = 20
        paragraphs, line_height = cap_text_to_max_height(tag[1], max_height, get_description_width() - config.ICON_LARGE_SIZE_PIXELS - self.icon_text_gap_px)
        text_total_height = get_paragraphs_height(paragraphs, line_height)
        self.paragraphs = paragraphs
        self.line_height = line_height
        self.height = max(config.ICON_LARGE_SIZE_PIXELS, text_total_height) + config.BLOCK_VERTICAL_PADDING * 2

    def render(self, img, d, y):
        icon_centered_y = y + self.height // 2 - config.ICON_LARGE_SIZE_PIXELS // 2
        text_centered_y = y + self.height // 2 - get_paragraphs_height(self.paragraphs, self.line_height) // 2
        x = config.TEXT_MARGIN
        if y > config.DESCRIPTION_Y_POSITION + config.DESCRIPTION_MAX_HEIGHT // 3:
            draw_horizontal_line(d, x + 20, y, get_description_width() - 40)
        draw_icon(img, x, icon_centered_y, self.icon)
        write_text(
            d,
            self.paragraphs, x + config.ICON_LARGE_SIZE_PIXELS + self.icon_text_gap_px, text_centered_y,
            get_description_width() - config.ICON_LARGE_SIZE_PIXELS - self.icon_text_gap_px,
            center=False,
            line_height=self.line_height
        )

    def height(self):
        return self.height
    

class TextBock(DescriptionBlock):

    def __init__(self, text, max_height):
        paragraphs, line_height = cap_text_to_max_height(text, max_height, get_description_width())
        text_total_height = get_paragraphs_height(paragraphs, line_height)
        self.paragraphs = paragraphs
        self.line_height = line_height
        self.height = text_total_height + config.BLOCK_VERTICAL_PADDING * 2

    def render(self, img, d, y):
        text_centered_y = y + self.height // 2 - get_paragraphs_height(self.paragraphs, self.line_height) // 2
        write_text(d, self.paragraphs, config.TEXT_MARGIN, text_centered_y, get_description_width(), True, self.line_height)
    
    def height(self):
        return self.height
    


def create_blocks(text: str) -> list[DescriptionBlock]:
    tags = []
    parsed_text = text
    for tag in config.TAGS:
        expr = f"<{tag}>(.*?)<\/{tag}>"
        maybeMatch = re.search(expr, parsed_text)
        if maybeMatch is None:
            continue
        # match.group(1) returns the text inside the regex capture group (parenthesis)
        inner_text = maybeMatch.group(1)
        tags.append([tag, inner_text])
        parsed_text = remove_tag_from_text(parsed_text, maybeMatch.span(0))

    blocks: list[DescriptionBlock] = []
    tags_row_block = [t for t in tags if t[0].lower() in ['steal', 'nut', 'lock']]
    tag_blocks = [t for t in tags if t[0].lower() in ['trap', 'pouch']]
    has_tag_row = len(tags_row_block) > 0
    has_text_block = len(parsed_text) > 0
    nof_tag_blocks = len(tag_blocks)
    height_without_tag_row = config.DESCRIPTION_MAX_HEIGHT - (config.ICON_LARGE_SIZE_PIXELS + config.BLOCK_VERTICAL_PADDING * 2 if has_tag_row else 0)
    if has_tag_row:
        blocks.append(TagsRowBlock(tags_row_block))
    if has_text_block:
        blocks.append(TextBock(parsed_text, height_without_tag_row // (1 + nof_tag_blocks)))
    for tag in tag_blocks:
        blocks.append(TagBlock(tag, height_without_tag_row // (nof_tag_blocks + (1 if has_text_block else 0))))  
    return blocks


def remove_tag_from_text(text: str, tag_pos: tuple[int, int]):
    return text[0:tag_pos[0]] + text[tag_pos[1]:len(text)]
