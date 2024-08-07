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
    'Steal',
    'Steals'
    'Trap:',
    'Trap',
    'Trash',
    'NUT!',
    'NUT',
    'NUTs',
    'EGG',
    'EGGs'
    'Pouch:',
    'Pouch',
    'Lock',
]
# Tags will be replaced with icons
# Write the name of the tag without any tag symbols, e.g. for <steal></steal> tags, write "steal"
TAGS = [
    'steal',
    'trap',
    'pouch',
    'nut',
    'lock',
]

# Directories
CARD_SAVE_DIR = 'generated_cards'
PICTURE_SOURCE_DIR = 'source_pictures'
TEMPLATES_DIR = 'templates/v3'
CREDENTIALS_PATH = 'credentials.json'
ICONS_DIR = 'icons'

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
EVENT_CARD_TYPES = ['eggvent', 'raid']
CARD_TYPES = ['EGG', 'trap', 'lock', 'steal', 'NUT'] + EVENT_CARD_TYPES

CARD_TYPES_WITH_ICONS = ['EGG', 'trap', 'lock']

TAB = 'Print sheet'
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
PIC_WIDTH = 615
PIC_HEIGHT = 585 
PIC_Y_POSITION = 133

# Icons
CARD_TYPE_ICON_SIZE_PIXELS = 90
CARD_TYPE_ICON_X = 30
CARD_TYPE_ICON_Y = 35

ICON_LARGE_SIZE_PIXELS = 105
ICON_LARGE_FONT = 'Mali-Bold.ttf'
ICON_LARGE_FONT_SIZE = 90
ICON_GUTTER = 20

# Title
TITLE_FONT_FILE = 'THURSTON_erc_002.ttf'
TITLE_FONTSIZE = 80
TITLE_Y_POSITION = 75
TITLE_MARGIN = 150
BREAK_TAG = '<br>'
BREAK_MIN_SIZE = 20 # Paragraph break

# COST
COST_X_POSITION = 600
COST_Y_POSITION = 60
COST_FONT_SIZE = 155
COST_FONT_FILE = 'THURSTON_erc_002.ttf'
NUT_SPACING = 54 # deprecated

# TYPE TEXT
CARD_TYPE_TEXT_X_POSITION = CARD_WIDTH_PIXELS // 2 + 5
CARD_TYPE_TEXT_Y_POSITION = 148
CARD_TYPE_TEXT_FONT = 'Onest-Bold.ttf'
CARD_TYPE_TEXT_FONT_SIZE = 22

# DESCRIPTION
DESCRIPTION_FONT_FILE = 'RobotoCondensed-Regular.ttf'
DESCRIPTION_FONT_BOLD_FILE = 'RobotoCondensed-Bold.ttf'
DESCRIPTION_FONTSIZE = 42
DESCRIPTION_LINE_HEIGHT = 46
DESCRIPTION_PARAGRAPH_BREAK_SIZE = 12
TEXT_MARGIN = 80
CHARACTERS_PER_ROW = 34 # deprecated
DESCRIPTION_Y_POSITION = 635
DESCRIPTION_MAX_HEIGHT = 320
BLOCK_VERTICAL_PADDING = 10

FLAVOUR_START_HEIGHT = CARD_HEIGHT_PIXELS - 300 # deprecated

# EVENT
EVENT_TITLE_FONTSIZE = 180
EVENT_TITLE_Y = 333
EVENT_DESCRIPTION_Y = 440

# Card grid generation
GENERATE_GRID = True
MAX_GRID_WIDTH = 5
MAX_GRID_HEIGHT = 2
MAX_CARDS = MAX_GRID_WIDTH * MAX_GRID_HEIGHT
X_PRINT_MARGIN_MM = 3
Y_PRINT_MARGIN_MM = 16
GRID_PDF_OUTPUT_FILE_NAME = "all_cards.pdf"
CARD_BACK_IMAGE_FULL_PATH = 'source_pictures/card_back.jpg'

