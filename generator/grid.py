from PIL import Image
import math
from utils import config


def combine_cards(cards):
    images = [Image.open(c) for c in cards]

    # Calculate final grid size
    nof_rows = math.ceil(len(images) / config.MAX_GRID_WIDTH)
    if len(images) > config.MAX_GRID_WIDTH:
        grid_size = (config.MAX_GRID_WIDTH * config.CARD_WIDTH_PIXELS,
                     nof_rows * config.CARD_HEIGHT_PIXELS)
    else:
        # Add an extra row to grids with only one row, required by Tabletop Simulator
        grid_size = (config.CARD_WIDTH_PIXELS * len(images),
                     config.CARD_HEIGHT_PIXELS * 2)
    card_grid = Image.new('RGB', grid_size)

    # Process batches of MAX_GRID_WIDTH
    for i in range(nof_rows):
        j = (i+1)*config.MAX_GRID_WIDTH if (i+1) * \
            config.MAX_GRID_WIDTH < len(images) else len(images)
        row = combine_rows(images[i * config.MAX_GRID_WIDTH:j])
        row_height = row.size[1]
        card_grid.paste(row, (0, i * row_height))
    return card_grid, grid_size


def combine_rows(images):
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    card_row = Image.new('RGBA', (total_width, max_height))

    x_offset = 0
    for im in images:
        card_row.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return card_row
