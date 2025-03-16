import alsaaudio

def change_volume(step):
    """
    Adjusts the system volume by a specified number of steps.
    
    :param step: The number of steps to increase or decrease the volume.
                 Positive for increasing volume, negative for decreasing.
    """
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

