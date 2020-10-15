# Possum game card generator

## Installation
`>pip3 install Pillow pandas`

## Setup
- Place source images in `source_pictures` directory.
- Place csv with correct columns in root directory.

## Usage
`> python3 generate_cards.py <name-of-card-csv-here.csv>`

You can tweak global constants in the beginning of the file to modify directory names, font sizes, position of text, etc.

## Expected fields in the csv
- Amount
- Tier (optional)
- Name
- Effect (optional)
- Card text (optional)
- Picture (optional)