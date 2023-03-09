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
]

# Directories
CARD_SAVE_DIR = 'generated_cards'
PICTURE_SOURCE_DIR = 'source_pictures'
TEMPLATES_DIR = 'templates'
CREDENTIALS_PATH = 'credentials.json'

# WINDOWS
FORBIDDEN_CHARACTERS = ['/', '\\', ':', '*', '?'
                        '\'', '<', '>', '|']

# -----------------
# GOOGLE API CONFIG
# -----------------

# Only set to false if you can't get the API to work for some reason
USE_GOOGLE_API = True

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
    'amount': 'Amount',
    'tier': 'Tier',
    'name': 'Name',
    'description': 'Effect',
    'flavour': 'Flavor text',
    'picture': 'Picture'
}

TAB = 'All cards'
RANGE = 'A1:F'
RANGE_NAME = f"'{TAB}'!{RANGE}"

# ---------------
# TEMPLATE CONFIG
# ---------------
# Card size in pixels
WIDTH = 700
HEIGHT = 1000

# Picture size
PIC_WIDTH = 660
PIC_HEIGHT = 550
PIC_Y_POSITION = 20

# Text
TEXT_LEFT_MARGIN = 50
TITLE_FONTSIZE = 60
TITLE_Y_POSITION = PIC_Y_POSITION + PIC_HEIGHT + 12
DESCRIPTION_FONTSIZE = 35
CHARACTERS_PER_ROW = 42
DESCRIPTION_Y_POSITION = TITLE_Y_POSITION + 100
FLAVOUR_START_HEIGHT = HEIGHT - 300

# Card grid generation
GENERATE_GRID = True
MAX_GRID_WIDTH = 3
MAX_GRID_HEIGHT = 3
MAX_CARDS = MAX_GRID_WIDTH * MAX_GRID_HEIGHT
