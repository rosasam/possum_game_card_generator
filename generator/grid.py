from PIL import Image
import math
import os
import glob

from utils import config


def generate_grid():
    tiers = filter(lambda d: '.' not in d, os.listdir(config.CARD_SAVE_DIR))
    for tier in tiers:
        cards = sorted(glob.glob(os.path.join(
            config.CARD_SAVE_DIR, tier, '*.png')))
        print(f'Generating grid for TIER: {tier.upper()}')
        # Process batches of 70
        for i in range(math.ceil(len(cards) / config.MAX_CARDS)):
            j = (i+1)*config.MAX_CARDS if (i+1) * \
                config.MAX_CARDS < len(cards) else len(cards)
            card_grid, grid_size = combine_cards(cards[i*config.MAX_CARDS:j])
            name = f'{tier}_{i+1}_{grid_size[0]//config.WIDTH}x{grid_size[1]//config.HEIGHT}_{len(cards)}.png'
            print(f'Saving {name}')
            card_grid.save(os.path.join(config.CARD_SAVE_DIR, name))


def combine_cards(cards):
    images = [Image.open(c) for c in cards]

    # Calculate final grid size
    nof_rows = math.ceil(len(images) / config.MAX_GRID_WIDTH)
    if len(images) > config.MAX_GRID_WIDTH:
        grid_size = (config.MAX_GRID_WIDTH * config.WIDTH,
                     nof_rows * config.HEIGHT)
    else:
        # Add an extra row to grids with only one row, required by Tabletop Simulator
        grid_size = (config.WIDTH * len(images), config.HEIGHT * 2)
    card_grid = Image.new('RGBA', grid_size)

    # Process batches of MAX_GRID_WIDTH
    for i in range(nof_rows):
        j = (i+1)*config.MAX_GRID_WIDTH if (i+1) * \
            config.MAX_GRID_WIDTH < len(images) else len(images)
        row = combine_rows(images[i*config.MAX_GRID_WIDTH:j])
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
