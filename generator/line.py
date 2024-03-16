from utils import config

def draw_horizontal_line(d, x, y, width, color="#26181477"):
    x = (config.CARD_WIDTH_PIXELS - width) // 2 if width < config.CARD_WIDTH_PIXELS else config.CARD_WIDTH_PIXELS
    shape = [(x, y), (width + x, y)] 
    d.line(shape, fill=color, width=2) 
