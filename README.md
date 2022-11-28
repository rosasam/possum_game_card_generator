# Possum game card generator

## Installation
`pip install --upgrade`  
`pip3 install -r requirements.txt`

## Setup
Card data and image files are pulled from Google Drive via Google Cloud API. You need to add client credentials for the service to your local repo.
The script needs access to GDrive metadata to search for image directories, GDrive read access to fetch the images and Sheets read access to fetch the card data.

1. Get the Google OAuth 2.0 Client credentials for Pouchin Possum from Google Cloud console (or ask the owner of this repo).  
2. Place the credentials in `utils/credentials.json`
3. Run the script!

## Usage
`> python3 generate_cards.py`

You can tweak global constants in `utils/config.py` to modify keywords, font sizes, position of text, etc.

## Expected fields in the csv
- Amount
- Tier (optional)
- Name
- Effect (optional)
- Flavour text (optional)
- Picture (optional)