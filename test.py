import os
import threading

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
import actions.open_application
import actions.open_website
from actions.actions import *
from configs.page_key_action_map import page_key_action_map

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")
def render_key_image(deck, page, key):



#def render_key_image(deck, icon_filename, font_filename, label_text):
    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.
    conf = page_key_action_map.get("pages").get(f"{page}".get("buttons").get(f"{key}"))
    icon = Image.open(icon_filename)

    icon_pressed = os.path.join(ASSETS_PATH, f"pages{page}/buttons/{key}/pressed.png")
    icon_released = os.path.join(ASSETS_PATH, f"pages{page}/buttons/{key}/released.png")

    print(f"icon paths = {icon_pressed}, {icon_released}")
    background = conf.get("display").get("background")
    font = ImageFont.truetype(font_filename, 14)

    pressed_image = PILHelper.create_scaled_key_image(deck, icon_pressed, margins=[0, 0, 20, 0], background=background)
    released_image = PILHelper.create_scaled_key_image(deck, icon_released, margins=[0, 0, 20, 0], background=background)
    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw = ImageDraw.Draw(image)
    
    draw.text((image.width / 2, image.height - 5), text=conf.get("name", "placeholder"), font=font, anchor="ms", fill="white")

    return PILHelper.to_native_key_format(deck, pressed_image)

print(f"image {render_key_image}")