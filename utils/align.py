from utils import config

def get_description_blocks_y_position(blocks):
    text_total_height = sum([len(line) for line in blocks]) * config.DESCRIPTION_LINE_HEIGHT + (len(blocks) - 1) * config.BREAK_MIN_SIZE
    if text_total_height > config.DESCRIPTION_MAX_HEIGHT:
        print( f'\033[93mWARNING\033[0m: Description too long to render completely, it will overflow.')

    text_height = min(text_total_height, config.DESCRIPTION_MAX_HEIGHT)
    extra_space = config.DESCRIPTION_MAX_HEIGHT - text_height
    vertical_padding = extra_space // (len(blocks) + 1)

    start_positions = []
    for i in range(len(blocks)):
        if i == 0:
            start_positions.append(vertical_padding)
        else:
            block_height = len(blocks[i - 1]) * config.DESCRIPTION_LINE_HEIGHT
            start_positions.append(block_height + vertical_padding + start_positions[i - 1] + config.BREAK_MIN_SIZE)

    return [s + config.DESCRIPTION_Y_POSITION for s in start_positions]
     