#!/usr/bin/env python3

#         Python Stream Deck Library
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

# Example script showing basic library usage - updating key images with new
# tiles generated at runtime, and responding to button state change events.

import os
import threading

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
import actions.open_application
import actions.open_website
from actions.actions import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib
import time
import json

WATCH_PATH = ".config"

# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")


class DeckHandler:
    def __init__(self, deck, profile, page, config_path):
        self.profile = profile
        self.page = page
        self.deck = deck
        self.config_path = config_path

    def load_config(self, config_path):
        d = os.path
        with open(config_path, "r") as f:
            conf = json.load(f)
            return conf

    def render_key_image(self, key):
        print("***"*10)
        print(f"reandering {self.profile} - {self.page}")
        print("***"*10)
        conf_dict = self.load_config(self.config_path)
        conf = conf_dict.get("pages").get(f"{self.page}").get("buttons").get(f"{key}")


        icon_pressed = Image.open(os.path.join(ASSETS_PATH, f"pages/{self.page}/buttons/{key}/pressed.png"))
        icon_released = Image.open(os.path.join(ASSETS_PATH, f"pages/{self.page}/buttons/{key}/released.png"))

        background = conf.get("display").get("background")
        font_filename = os.path.join(ASSETS_PATH, f"fonts/Roboto-Regular.ttf")
        font = ImageFont.truetype(font_filename, 14)


        pressed_image = PILHelper.create_scaled_key_image(self.deck, icon_pressed, margins=[0, 0, 20, 0], background=background)
        released_image = PILHelper.create_scaled_key_image(self.deck, icon_released, margins=[0, 0, 20, 0], background=background)
        # Load a custom TrueType font and use it to overlay the key index, draw key
        # label onto the image a few pixels from the bottom of the key.
        draw_pressed = ImageDraw.Draw(pressed_image)
        draw_released = ImageDraw.Draw(released_image)
        
        draw_pressed.text((pressed_image.width / 2, pressed_image.height - 5), text=conf.get("name", "placeholder"), font=font, anchor="ms", fill="white")
        draw_pressed.text((released_image.width / 2, released_image.height - 5), text=conf.get("name", "placeholder"), font=font, anchor="ms", fill="white")

        return PILHelper.to_native_key_format(self.deck, pressed_image)


    def update_key_image(self, key):
        # Determine what icon and label to use on the generated key.
        #key_style = get_key_style(deck,page, key, state)

        # Generate the custom key with the requested image and label.
        image = self.render_key_image(key)

        # Use a scoped-with on the deck to ensure we're the only thread using it
        # right now.
        with self.deck:
            # Update requested key with the generated image.
            self.deck.set_key_image(key, image)  

    def render_full_page(self):
        for key in range(self.deck.key_count()):
            self.update_key_image(key)
        

    def key_change_callback(self, deck, key, state):
        if key == 14 and state == True:

            print("next page key TODO handle graciously")
            
            self.page = f"{int(self.page) + 1}"
            self.render_full_page()
        print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)
        
        # Don't try to draw an image on a touch button
        if key > deck.key_count():
            return

        # Update the key image based on the new key state.
        self.update_key_image(key)

        # Check if the key is changing to the pressed state.
        if state:
            if state == True:
                conf = self.load_config(self.config_path)
                acts = list(conf.get("pages").get(f"{self.page}").get("buttons").get(f"{key}").get("actions").items())
                perform_action(acts)     

def main():
    streamdecks = DeviceManager().enumerate()
    state = {
        "profile": "default",
        "page": "1"
    }

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        deckhandler = DeckHandler(deck, state.get("profile", 1), state.get("page", "default"), "configs/page_key_action_map.json")
        deck.close()
        # This example only works with devices that have screens.
        if not deck.is_visual():
            continue
        try:
            deck.open()
            deck.reset()
        except Exception as e:
            print("Error opening deck. {e}")
            deck.close()
            deck.open()

        print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
            deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        ))

        # Set initial screen brightness to 30%.
        deck.set_brightness(30)

        # Set initial key images.
        deckhandler.render_full_page()

        # Register callback function for when a key state changes.
        deck.set_key_callback(deckhandler.key_change_callback)

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                pass


# if __name__ == "__main__":
#     main()