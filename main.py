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
from configs.page_key_action_map import page_key_action_map

# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")


# Generates a custom tile with run-time generated text and custom image via the
# PIL module.
def render_key_image(deck, page, key):



#def render_key_image(deck, icon_filename, font_filename, label_text):
    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.
    conf = page_key_action_map.get("pages").get(f"{page}").get("buttons").get(f"{key}")
    print("----"*10)
    print(f"conf = {conf}")
    print("----"*10)
    print(f"page = {page}, key= {key}")

    print("----"*10)


    icon_pressed = Image.open(os.path.join(ASSETS_PATH, f"pages/{page}/buttons/{key}/pressed.png"))
    icon_released = Image.open(os.path.join(ASSETS_PATH, f"pages/{page}/buttons/{key}/released.png"))

    print(f"icon paths = {icon_pressed}, {icon_released}")
    background = conf.get("display").get("background")
    font_filename = os.path.join(ASSETS_PATH, f"fonts/Roboto-Regular.ttf")
    font = ImageFont.truetype(font_filename, 14)


    pressed_image = PILHelper.create_scaled_key_image(deck, icon_pressed, margins=[0, 0, 20, 0], background="white")
    released_image = PILHelper.create_scaled_key_image(deck, icon_released, margins=[0, 0, 20, 0], background="white")
    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw_pressed = ImageDraw.Draw(pressed_image)
    draw_released = ImageDraw.Draw(released_image)
    
    draw_pressed.text((pressed_image.width / 2, pressed_image.height - 5), text=conf.get("name", "placeholder"), font=font, anchor="ms", fill="white")
    draw_pressed.text((released_image.width / 2, released_image.height - 5), text=conf.get("name", "placeholder"), font=font, anchor="ms", fill="white")

    return PILHelper.to_native_key_format(deck, pressed_image)




# Returns styling information for a key based on its position and state.
def get_key_style(deck, page, key, state):
    # Last button in the example application is the exit button.
    exit_key_index = deck.key_count() - 1

    if key == exit_key_index:
        name = "exit"
        icon = "{}.png".format("Exit")
        font = "Roboto-Regular.ttf"
        label = "Bye" if state else "Exit"
    else:
        name = "emoji"
        icon = "pages/{}/buttons/{}/{}.png".format(page,key,"pressed" if state else "released")
        font = "Roboto-Regular.ttf"
        label = "pressed!" if state else "Key {}".format(key)

    return {
        "name": name,
        "icon": os.path.join(ASSETS_PATH, icon),
        "font": os.path.join(ASSETS_PATH, font),
        "label": label
    }


# Creates a new key image based on the key index, style and current key state
# and updates the image on the StreamDeck.
def update_key_image(deck, page, key, state):
    # Determine what icon and label to use on the generated key.
    #key_style = get_key_style(deck,page, key, state)

    # Generate the custom key with the requested image and label.
    image = render_key_image(deck, page, key)

    # Use a scoped-with on the deck to ensure we're the only thread using it
    # right now.
    with deck:
        # Update requested key with the generated image.
        deck.set_key_image(key, image)


# Prints key state change information, updates rhe key image and performs any
# associated actions when a key is pressed.
def key_change_callback(deck, key, state):
    print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)
    
    # Don't try to draw an image on a touch button
    if key > deck.key_count():
        return

    # Update the key image based on the new key state.
    update_key_image(deck, 1, key, state)

    # Check if the key is changing to the pressed state.
    if state:
        if state == True:
            acts = get_all_actions(1, key)
            print(f"--"*10)
            print(f"{acts}")
            print(f"--"*10)
            perform_action(acts)
        print(f"state = {state}")
        # key_style = get_key_style(deck, 1, key, state)

        # # When an exit button is pressed, close the application.
        # if key_style["name"] == "exit":
        #     # Use a scoped-with on the deck to ensure we're the only thread
        #     # using it right now.
        #     with deck:
        #         # Reset deck, clearing all button images.
        #         deck.reset()

        #         # Close deck handle, terminating internal worker threads.
        #         deck.close()


if __name__ == "__main__":

    streamdecks = DeviceManager().enumerate()

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        # This example only works with devices that have screens.
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
            deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        ))

        # Set initial screen brightness to 30%.
        deck.set_brightness(30)

        # Set initial key images.
        for key in range(deck.key_count()):
            update_key_image(deck, 1, key, False)

        # Register callback function for when a key state changes.
        deck.set_key_callback(key_change_callback)

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                pass