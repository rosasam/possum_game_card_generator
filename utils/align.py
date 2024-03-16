from utils import config

def get_description_blocks_y_position(blocks):
    total_height = sum(b.height for b in blocks)
    if total_height > config.DESCRIPTION_MAX_HEIGHT:
        print( f'\033[93mWARNING\033[0m: Description too long to render completely, it will overflow.')

    total_height = min(total_height, config.DESCRIPTION_MAX_HEIGHT)
    extra_space = config.DESCRIPTION_MAX_HEIGHT - total_height
    vertical_padding = extra_space // (len(blocks) + 1)

    start_positions = []
    for i in range(len(blocks)):
        if i == 0:
            start_positions.append(vertical_padding)
        else:
            start_positions.append( start_positions[i - 1] + blocks[i-1].height + vertical_padding)

    return [s + config.DESCRIPTION_Y_POSITION for s in start_positions]

def get_paragraphs_height(paragraphs, line_height=config.DESCRIPTION_LINE_HEIGHT):
    return sum([len(lines) for lines in paragraphs]) * line_height + (len(paragraphs) - 1) * config.BREAK_MIN_SIZE

def get_description_width() -> int:
    return config.CARD_WIDTH_PIXELS - config.TEXT_MARGIN * 2
