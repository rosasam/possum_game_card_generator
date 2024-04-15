import os

def create_pic_file_name(pic_name: str) -> str:
  """Creates the image file name from the name of the image"""
  return f"{pic_name.lower().replace(' ', '_')}.jpg"