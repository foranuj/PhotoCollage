import os
import getpass

from PIL import ImageFont

FONT_DIR = os.path.join("/Users", getpass.getuser(), "GoogleDrive", "Fonts")
TITLE_FONT_OPEN_SANS = ImageFont.truetype(os.path.join(FONT_DIR, "open-sans/OpenSans-Bold.ttf"), 100)
TEXT_FONT_SMALL = ImageFont.truetype(os.path.join(FONT_DIR, "open-sans/OpenSans-Bold.ttf"), 50)
TITLE_FONT_MOHAVE = ImageFont.truetype(os.path.join(FONT_DIR, "Mohave/Mohave-SemiBold.ttf"), 100)
TITLE_FONT_SELIMA = ImageFont.truetype(os.path.join(FONT_DIR, "selima/selima_.otf"), 135)
TITLE_FONT_ECZAR = ImageFont.truetype(os.path.join(FONT_DIR, "Eczar", "static", "Eczar-SemiBold.ttf"), 105)