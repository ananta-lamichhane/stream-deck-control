import os
import threading

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
import actions.open_application
import actions.open_website
from actions.actions import *
from actions.action import Action
import importlib
import time
import json



# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")


class DeckHandler:
    def __init__(self, deck, profile, page, config_path, brightness):
        self.profile = profile
        self.page = page
        self.deck = deck
        self.config_path = config_path
        self.brightness = brightness
    ## setters
    def set_brightness(self):
        self.brightness = brightness
    def set_page(self):
        self.page = page
    def set_deck(self):
        self.deck = deck
    def set_config_path(self):
        self.config_path = config_path
    def set_profile(self):
        self.profile = profile
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

    def render_key_image(self, key):
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
        conf = self.load_config(self.config_path)
        key_conf = conf.get("pages").get(f"{self.page}").get("buttons").get(f"{key}").get("actions").items()
        print(f"{key_conf}")
        for i in key_conf:  
            act = Action(i[0], key, "deck", i[1])
            if state == True:
                act.perform_action()
                # if state == True:
                #     conf = self.load_config(self.config_path)
                #     acts = list(conf.get("pages").get(f"{self.page}").get("buttons").get(f"{key}").get("actions").items())
                #     perform_action(acts)     
