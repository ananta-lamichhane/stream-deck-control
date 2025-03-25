import sys
import alsaaudio
import subprocess



class Action:
    def __init__(self, name, key, act_target, args):
        self.name = name
        ## is the action targeted towards deck, system, applications or something else
        self.act_target = act_target
        self.key = key
        ## string with comma separated values
        self.args = args
    
    def perform_action(self):
        raise NotImplementedError("Subclasses must implement this method")



class OpenApplicationAction(Action):
    def __init__(self,  key, args):
        super().__init__("open_application", key, "app", args)
    
    def perform_action(self):
        ## since opening only one application args should only have one element
        args_str = self.args.split(",")
        app_to_open = args_str[0]
        try:
            subprocess.run([f"{app_to_open}"], check=True)
            print(f"{app_to_open} opened successfully.")
        except FileNotFoundError:
            print(f"{app_to_open} is not installed or not in the system PATH.")
        except subprocess.CalledProcessError:
            print(f"An error occurred while trying to open {app_to_open}.")


class ChangeVolumeAction(Action):
    def __init__(self,  key, args):
        super().__init__("change_volume", key, "sys", args)

    
    def perform_action(self):
        """
        Adjusts the system volume by a specified number of steps.
        
        :param step: The number of steps to increase or decrease the volume.
                    Positive for increasing volume, negative for decreasing.
        """
        ## volume wil be given as arg string
        args_str = self.args.split(",")
        step = args_str[0]
        try:
            # Open the default mixer
            mixer = alsaaudio.Mixer()

            # Get the current volume (returns a tuple of the min and max values and the current value)
            current_volume = mixer.getvolume()[0]

            # Calculate new volume
            new_volume = current_volume + int(step)

            # Ensure the volume is within the valid range (0-100)
            if new_volume > 100:
                new_volume = 100
            elif new_volume < 0:
                new_volume = 0

            # Set the new volume
            mixer.setvolume(new_volume)

            print(f"Volume changed to {new_volume}%")
        
        except alsaaudio.ALSAAudioError as e:
            print(f"Failed to get or set volume: {e}")

class OpenWebsiteAction(Action):
    def __init__(self, key, args):
        super().__init__("change_volume", key, "app", args)

    def perform_action(self):
        browser = "firefox" ## TODO: make it adjustable
        args_str = self.args.split(",")
        website = args_str[0]
        subprocess.run([browser, website])


class ChangePageAction(Action):
    def __init__(self, key, args):
        super().__init__("change_page", key, "deck", args)
        self.deck = None

    def perform_action(self):
        args_str = self.args.split(",")
        page_no = args_str[0]
        ## send deck attribute that to be chaned and value
        self.deck.set_page(page_no)
        
    def set_deck(self, deck):
        self.deck = deck

class ChangeDeckBrightnessAction(Action):
    def __init__(self, key, args):
        super().__init__("change_page", key, "deck", args)
        self.deck = None

    def perform_action(self):
        args_str = self.args.split(",")
        br = args_str[0]
        ## send deck attribute that to be chaned and value
        self.deck.set_brightness(br)
        
    def set_deck(self, deck):
        self.deck = deck