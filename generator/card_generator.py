import os
from utils import config
from generator.cards import add_layer, add_picture, write_description, write_title, add_nuts, write_lock_modifier
from generator.card import Card
from fpdf import FPDF
from PIL import Image, ImageDraw
import math
import re

class Generator:

    def __init__(self, testmode=False):
        self.cards = []
        self.testmode = testmode

    def add_card(self, card: Card):
        self.cards.append(card)

    def get_all_card_image_file_paths(self):
        all_card_paths = []
        for card in self.cards:
            for i in range(card.amount):
                all_card_paths.append(card.card_image_full_path)
        return all_card_paths

    def generate_card(self, card: Card, full_output_path: str):
        # TODO: Split into more functions (maybe split into image manipulator class?)
        card_image = Image.new(
            'RGBA', (config.CARD_WIDTH_PIXELS, config.CARD_HEIGHT_PIXELS))

        add_layer(card_image, 'bottom', card.type)

        if card.picture_file_name:
            try:
                picture_file_path = os.path.join(config.PICTURE_SOURCE_DIR,
                                                 card.picture_file_name)
                add_picture(card_image, picture_file_path)
            except Exception as e:
                print(
                    f'\033[93mWARNING\033[0m: Picture file \"{picture_file_path}\" for card \"{card.name}\" could not be found.'
                )
        add_layer(card_image, 'top', card.type)

        d = ImageDraw.Draw(card_image)
        #write_nut_cost(card_image, d, card.cost)
        add_nuts(card_image, card.cost)
        write_title(d, card.name)

        if card.description:
            write_description(d, card.description)

        if card.type == 'lock':
            lock_modifier = re.findall("Protect (\+[0-9])", card.description)
            lock_modifier = lock_modifier[0] if len(lock_modifier) > 0 else '?'
            write_lock_modifier(d, lock_modifier)

        card_image.save(f'{full_output_path}.png')
        card.card_image_full_path = f'{full_output_path}.png'
        if self.testmode:
            card_image.show()

    def generate_cards(self):
        for card in self.cards:
            card_file_name = card.get_card_file_name()
            cardpath = os.path.join(config.CARD_SAVE_DIR, card_file_name)

            print(f'Generating {card_file_name}')
            self.generate_card(card, cardpath)

    def generate_grid_pdf(self):
        pdf = FPDF(orientation="landscape", format="A4", unit='mm')
        all_card_paths = self.get_all_card_image_file_paths()
        cards_per_page = config.MAX_GRID_WIDTH * config.MAX_GRID_HEIGHT
        total_card_amount = len(all_card_paths)
        nof_pages_needed = math.ceil(total_card_amount / cards_per_page)
        for page_number in range(nof_pages_needed):
            pdf.add_page()
            card_amount_on_page = total_card_amount - page_number * cards_per_page
            for j in range(config.MAX_GRID_HEIGHT):
                image_position_y = config.Y_PRINT_MARGIN_MM + j * config.CARD_HEIGHT_MM
                for i in range(config.MAX_GRID_WIDTH):
                    # Stop if we've printed all cards
                    if j * config.MAX_GRID_WIDTH + i >= card_amount_on_page:
                        break

                    image_position_x = config.X_PRINT_MARGIN_MM + i * config.CARD_WIDTH_MM
                    index_of_image = page_number * cards_per_page + j * config.MAX_GRID_WIDTH + i
                    pdf.image(all_card_paths[index_of_image],
                              x=image_position_x,
                              y=image_position_y,
                              w=config.CARD_WIDTH_MM,
                              h=config.CARD_HEIGHT_MM)

            self.generate_card_back_page(pdf, card_amount_on_page)
        pdf.output(
            os.path.join(config.CARD_SAVE_DIR,
                         config.GRID_PDF_OUTPUT_FILE_NAME))

    def generate_card_back_page(self, pdf, card_amount_on_page):
        # Add card back
        pdf.add_page()
        for j in range(config.MAX_GRID_HEIGHT):
            image_position_y = config.Y_PRINT_MARGIN_MM + j * config.CARD_HEIGHT_MM
            for i in range(config.MAX_GRID_WIDTH):
                image_position_x = config.X_PRINT_MARGIN_MM + i * config.CARD_WIDTH_MM
                pdf.image(config.CARD_BACK_IMAGE_FULL_PATH,
                          x=image_position_x,
                          y=image_position_y,
                          w=config.CARD_WIDTH_MM,
                          h=config.CARD_HEIGHT_MM)
