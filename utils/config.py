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
        'name': 'EGG',
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

# Google sheets field name as value, don't change the keys!
GOOGLE_SHEETS_FIELD_NAMES = {
    'amount': 'Amount',
    'tier': 'Tier',
    'name': 'Name',
    'description': 'Effect',
    'flavour': 'Flavor text',
    'picture': 'Picture'
}

# Directories
CARD_SAVE_DIR = 'generated_cards'
PICTURE_SOURCE_DIR = 'source_pictures'
TEMPLATES_DIR = 'templates'
CREDENTIALS_PATH = 'credentials.json'

# Card grid generation
GENERATE_GRID = True
MAX_GRID_WIDTH = 10
MAX_GRID_HEIGHT = 7
MAX_CARDS = MAX_GRID_WIDTH * MAX_GRID_HEIGHT

# WINDOWS
FORBIDDEN_CHARACTERS = ['/', '\\', ':', '*', '?' '\'', '<', '>', '|']

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
