from utils import config
from PIL import ImageFont
import os

class Word:
    def __init__(self, text: str, fontStyle: str, space_after: int, fontsize):
        if (fontStyle == 'bold'):
            self.font = ImageFont.truetype(os.path.join('fonts', config.DESCRIPTION_FONT_BOLD_FILE), fontsize)
        else:
            self.font = ImageFont.truetype(os.path.join('fonts', config.DESCRIPTION_FONT_FILE), fontsize)
        self.text = text
        self.space_after = space_after
        self.length = self.font.getsize(text)[0] + space_after
    
    
# Splits words into lines, and lines into paragraphs (based on break tag)
def text_wrap(words, max_width: int):
    paragraphs = []
    lines = []
    current_line = words[0:1]
    for word in words[1:]:
        if word.text == config.BREAK_TAG:
            lines.append(current_line)
            #paragraphs.append(lines)
            #lines = []
            current_line = []
        elif sum([w.length for w in current_line]) + word.length < max_width:
            current_line.append(word)
        else:
            lines.append(current_line)
            current_line = [word]
    lines.append(current_line)
    paragraphs.append(lines)

    return paragraphs

# Words can have punctuation marks at the end
 # assign properties to words: bold, line break, space after, etc. join non-breaking words together
def encode_text(text, fontsize=config.DESCRIPTION_FONTSIZE, keywords=config.KEYWORDS):
    words = text.split(' ')
    keywords_lower = [k.lower() for k in keywords]
    encoded_words = []
    # Increase font size for cards with very little text.
    fontsize = int(fontsize * 1.2) if len(words) < 5 else fontsize

    for word in words:
        style = 'bold' if word.lower().replace('.', '').replace(',', '') in keywords_lower else 'regular'
        encoded_words.append(Word(word, style, 8, fontsize))
    return encoded_words

def write_text(d, paragraphs, x, y, width, center=True, line_height=config.DESCRIPTION_LINE_HEIGHT):
    y_position = y
    for lines in paragraphs:
        for line in lines:
            linewidth = sum([w.length for w in line])
            x_position = x
            if center:
                x_position = int(x + width / 2 - linewidth / 2)
            for word in line:
                d.text((x_position, y_position), word.text, fill='black', font=word.font)
                x_position += word.length
            y_position += line_height
        y_position += config.BREAK_MIN_SIZE
    return y_position


def cap_text_to_max_height(text: str, max_height: int, text_width: int):
    total_height = 10000000
    line_height = config.DESCRIPTION_LINE_HEIGHT
    font_size = config.DESCRIPTION_FONTSIZE
    paragraphs = []
    while total_height > max_height:
        words = encode_text(text, font_size)
        paragraphs = text_wrap(words, text_width)
        total_height = len(paragraphs[0]) * line_height
        if total_height > max_height:
            line_height = int(line_height / 1.1)
            font_size = int(font_size / 1.1)
    return paragraphs, line_height