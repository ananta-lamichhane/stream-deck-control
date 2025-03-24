from StreamDeck.DeviceManager import DeviceManager
import threading
from deckhandler import DeckHandler


def main():
    streamdecks = DeviceManager().enumerate()

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        deckhandler = DeckHandler(deck, "default", "1", "configs/page_key_action_map.json", 30)
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
        deck.set_brightness(deckhandler.get_brightness())

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
if __name__ == "__main__":
    main()