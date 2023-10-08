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
    
# Splits words into lines, and lines into blocks (based on break tag)
def text_wrap(words, max_width: int):
    blocks = []
    lines = []
    current_line = words[0:1]
    for word in words[1:]:
        if word.text == config.BREAK_TAG:
            lines.append(current_line)
            blocks.append(lines)
            lines = []
            current_line = []
        elif sum([w.length for w in current_line]) + word.length < max_width:
            current_line.append(word)
        else:
            lines.append(current_line)
            current_line = [word]
    lines.append(current_line)
    blocks.append(lines)

    return blocks

# Words can have punctuation marks at the end
 # assign properties to words: bold, line break, space after, etc. join non-breaking words together
def encode_words(words, keywords, fontsize):
    keywords_lower = [k.lower() for k in keywords]
    encoded_words = []
    # Increase font size for cards with very little text.
    fontsize = int(fontsize * 1.2) if len(words) < 5 else fontsize

    for word in words:
        style = 'bold' if word.lower().replace('.', '').replace(',', '') in keywords_lower else 'regular'
        encoded_words.append(Word(word, style, 8, fontsize))
    return encoded_words


        