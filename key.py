import glob
import os
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from actions import action

class Key:
    def __init__(self, number, state, image_path, deck, label, background):
        self.number = number
        self.state = state
        self.image_path = image_path
        self.deck = deck
        self.label = label
        self.background = background
        #self.action = action

    def render_key_image(self):
        
        icon_dir = self.image_path
        p_or_r = "*_pressed" if self.state == True else "*_released"

        try:
            icon_multi = glob.glob(os.path.join(self.image_path, p_or_r ))
            icon = Image.open(icon_multi[0])
            image = PILHelper.create_scaled_key_image(self.deck, icon, margins=[0, 0, 20, 0], background=self.background)
            
            return PILHelper.to_native_key_format(self.deck, image)
        except Exception as e:
            print(f"{e}")
            print("pressed / rleased image not found, loading single image for both")
            icon_single_multi = glob.glob(os.path.join(icon_dir, "*.png" ))
            icon = Image.open(icon_single_multi[0])
            single_image = PILHelper.create_scaled_key_image(self.deck.deck, icon, margins=[0, 0, 20, 0], background=self.background)

            return PILHelper.to_native_key_format(self.deck.deck, single_image)
            

    def update_key_image(self, state):
        image = self.render_key_image()
        self.deck.deck.set_key_image(self.number, image)
    
    def action(self, config, page):
        conf = config
        key_conf = conf.get("pages").get(f"{page}").get("buttons").get(f"{self.number}").get("actions").items()
        for i in key_conf:
            if self.state == True:
                class_name = f"{i[0]}Action"
                cl = getattr(action, class_name)
                act = cl(self.number, i[1])      
                if act.act_target == "deck":
                    act.set_deck(self.deck)
                    act.perform_action()
                    self.deck.render_full_page()
                else:
                    act.perform_action()
            