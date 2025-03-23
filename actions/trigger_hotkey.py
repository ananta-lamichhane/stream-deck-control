from evdev import UInput, ecodes as e

# Create a mapping of character to evdev key codes
# https://github.com/holoplot/go-evdev/blob/master/codes.go
key_map = {
    'a': e.KEY_A,
    'b': e.KEY_B,
    'c': e.KEY_C,
    'd': e.KEY_D,
    'e': e.KEY_E,
    'f': e.KEY_F,
    'g': e.KEY_G,
    'h': e.KEY_H,
    'i': e.KEY_I,
    'j': e.KEY_J,
    'k': e.KEY_K,
    'l': e.KEY_L,
    'm': e.KEY_M,
    'n': e.KEY_N,
    'o': e.KEY_O,
    'p': e.KEY_P,
    'q': e.KEY_Q,
    'r': e.KEY_R,
    's': e.KEY_S,
    't': e.KEY_T,
    'u': e.KEY_U,
    'v': e.KEY_V,
    'w': e.KEY_W,
    'x': e.KEY_X,
    'y': e.KEY_Y,
    'z': e.KEY_Z,
    '1': e.KEY_1,
    '2': e.KEY_2,
    '3': e.KEY_3,
    '4': e.KEY_4,
    '5': e.KEY_5,
    '6': e.KEY_6,
    '7': e.KEY_7,
    '8': e.KEY_8,
    '9': e.KEY_9,
    '0': e.KEY_0,
    'enter': e.KEY_ENTER,
    'esc': e.KEY_ESC,
    'backspace': e.KEY_BACKSPACE,
    'ctrl': e.KEY_LEFTCTRL,
    'space': e.KEY_SPACE,
    'tab': e.KEY_TAB,
    'alt': e.KEY_LEFTALT,
    'shift': e.KEY_LEFTSHIFT,
    "space": e.KEY_SPACE,
    "asterisk": e.KEY_KPASTERISK,
    "semicolon":  e.KEY_SEMICOLON,
	"apostrophe": e.KEY_APOSTROPHE,
    'left': e.KEY_LEFT,
    'right': e.KEY_RIGHT,
    'up': e.KEY_UP,
    'down': e.KEY_DOWN,
    'win': e.KEY_LEFTMETA
    # Add more key mappings as needed
}

def trigger_hotkey(keys: str):
    # Parse the input string and split by '+'
    key_sequence = keys.split('+')

    # Create a virtual input device
    with UInput() as ui:
        for key in key_sequence:
            if key in key_map:
                # Press the key
                ui.write(e.EV_KEY, key_map[key], 1)
                ui.syn()
               

        # Release the keys
        for key in reversed(key_sequence):
            if key in key_map:
                ui.write(e.EV_KEY, key_map[key], 0)
                ui.syn()  # Synchronize the event

# Example usage:
#trigger_hotkey("e+c+h+o+space+a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+enter")
