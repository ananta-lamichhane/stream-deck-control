# stream-deck-control
Minimal stream deck control interface for linux

## Motivation
As existing linux clients for Stream Deck are not particularly functional,I decided making my own using the `streamdeck` python module. As of now, there is no GUI. Just a config file to configure the look and function of each individual keys.

## How to use
1. Clone this git repo.
2. Create a python3 virtual environment on the root of the project `python3 -m venv venv`.
3. Activate venv `source venv/bin/activate`.
4. Install requirments `pip install -r requirements.txt`.
5. Use configs -> page_key_activation_map.py to configure the buttons and their functionalities.
6. Use `python3 main.py` to run the main script.
7. Use appropriate methods to run it in the background if necessary.

## Current Functionality
1. Open system applications (must be callable using their name on terminal e.g. `firefox`, `google-chrome`, etc.)
2. Open arbitrary website (on firefox currently but can be configured).
3. Turn system volume up and down.

## Upcoming functionality
1. Support multiple pages.
2. Support profiles.
3. Support nested folders.
4. Support dynamic switching to profiles based on button press.
NOTE: Please note no particular timeline is set for upcoming functinalities.

