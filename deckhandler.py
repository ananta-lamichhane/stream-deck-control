import os
import threading

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from actions import action
import importlib
import time
import json
import glob

from key import Key


# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")


class DeckHandler:
    def __init__(self, deck, profile, page, config_path, brightness):
        self.profile = profile
        self.page = page
        self.deck = deck
        self.config_path = config_path
        self.brightness = brightness

        self.deck.close()
        # This example only works with devices that have screens.
        try:
            self.deck.open()
            self.deck.reset()
        except Exception as e:
            print("Error opening deck. {e}")
            self.deck.close()
            self.deck.open()
    
    ## setters
    def set_brightness(self, new_brightness):
        self.brightness = new_brightness
    def set_page(self, new_page):
        self.page = new_page
    def set_deck(self, new_deck):
        self.deck = new_deck
    def set_config_path(self, new_config_path):
        self.config_path = new_config_path
    def set_profile(self, new_profile):
        self.profile = new_profile
    ##getters
    def get_brightness(self):
        return self.brightness
    def get_page(self):
        return self.page
    def get_key_style_deck(self):
        return self.deck
    def get_config_path(self):
        return self.config_path
    def get_profile(self):
        return self.profile

    def load_config(self, config_path):
        d = os.path
        with open(config_path, "r") as f:
            conf = json.load(f)
            return conf

    def render_full_page(self):
        for i in range(self.deck.key_count()):
            img_path = os.path.join(ASSETS_PATH, f"pages/{self.page}/buttons/{i}")
            k = Key(i, False, img_path, self, "label", "white")
            k.update_key_image(False)
        
            
    def key_change_callback(self, deck, key, state):
        print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)
        
        # Don't try to draw an image on a touch button
        if key > deck.key_count():
            return

        # Update the key image based on the new key state.
        #for i in range(self.deck.key_count()):
        img_path = os.path.join(ASSETS_PATH, f"pages/{self.page}/buttons/{key}")
        k = Key(key, state, img_path, self, "label", "red")
        k.update_key_image(False)
        conf = self.load_config(self.config_path)
        k.action(conf, self.page)
