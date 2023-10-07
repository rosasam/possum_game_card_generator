TIERS = {
    0: {
        'name': 'base',
        'color': (194, 223, 227)
    },
    1: {
        'name': 'common',
        'color': (242, 204, 143)  # beige
    },
    2: {
        'name': 'rare',  # blue
        'color': (76, 201, 240),
    },
    3: {
        'name': 'epic',  # purple
        'color': (240, 80, 174),
    },
    4: {
        'name': 'legendary',  # gold
        'color': (253, 241, 72),
    },
    10: {
        'name': 'egg',
        'color': 'white',
    }
}

# Keywords in the description will be bolded
KEYWORDS = [
    'Take',
    'Discard',
    'Age',
    'Steal',
    'Stash',
    'Peek',
    'Trap',
    'Draw',
    'Gain',
    'Trash',
    'NUT!',
    'EGG',
    'Pouch',
]

# Directories
CARD_SAVE_DIR = 'generated_cards'
PICTURE_SOURCE_DIR = 'source_pictures'
TEMPLATES_DIR = 'templates/v2'
CREDENTIALS_PATH = 'credentials.json'

# WINDOWS
FORBIDDEN_CHARACTERS = ['/', '\\', ':', '*', '?'
                        '\'', '<', '>', '|']

# -----------------
# GOOGLE API CONFIG
# -----------------

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

DRIVE_SOURCE_IMAGE_DIR_ID = '1bk23hNSETw9zm8u1-3My8zY0IRJkFBrr'

# 'All cards' spreadsheet ID
SPREADSHEET_ID = '1yJsNpidAPBM8KogZp611Ebn-r0iaY9_1g5bkOW0XOM0'

# Google sheets field name as value, don't change the keys!
GOOGLE_SHEETS_FIELD_NAMES = {
    'cost': '$',
    'amount': 'Amount',
    'type': 'Type',
    'name': 'Name',
    'description': 'Effect',
    'flavour': 'Flavor text'
}
# Special card types. These should match the naming of their corresponding card image files
# e.g. card_template_top_EGG
CARD_TYPES = ['EGG', 'trap', 'lock']

TAB = 'All cards'
RANGE = 'A1:G'
RANGE_NAME = f"'{TAB}'!{RANGE}"

# ---------------
# TEMPLATE CONFIG
# ---------------
# Card size in pixels
PPI = 300
PPMM = PPI / 25.4
CARD_WIDTH_MM = 58
CARD_HEIGHT_MM = 89
CARD_WIDTH_PIXELS = int(CARD_WIDTH_MM * PPMM)
CARD_HEIGHT_PIXELS = int(CARD_HEIGHT_MM * PPMM)

# Picture size
PIC_WIDTH = 648
PIC_HEIGHT = 570
PIC_Y_POSITION = 24

# Text
TEXT_LEFT_MARGIN = 50
TITLE_FONT_FILE = 'THURSTON_erc_002.ttf'
TITLE_FONTSIZE = 60
TITLE_Y_POSITION = PIC_Y_POSITION + PIC_HEIGHT + 20
COST_POSITION_Y = 45
DESCRIPTION_FONTSIZE = 35
CHARACTERS_PER_ROW = 42
DESCRIPTION_Y_POSITION = TITLE_Y_POSITION + 100
FLAVOUR_START_HEIGHT = CARD_HEIGHT_PIXELS - 300

# Card grid generation
GENERATE_GRID = True
MAX_GRID_WIDTH = 5
MAX_GRID_HEIGHT = 2
MAX_CARDS = MAX_GRID_WIDTH * MAX_GRID_HEIGHT
X_PRINT_MARGIN_MM = 3
Y_PRINT_MARGIN_MM = 16
GRID_PDF_OUTPUT_FILE_NAME = "all_cards.pdf"
CARD_BACK_IMAGE_FULL_PATH = 'source_pictures/card_back.jpg'