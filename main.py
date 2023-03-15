import pyperclip
import time
import io
import pygame
import keyboard
import threading
import pyttsx3
from gtts import gTTS

choice = input('Chose your language (English for en) (Bangla for bn) only work on Online :')

language = choice

def offlineAudio(text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set the properties for the voice
    voice = engine.getProperty('voices')[0]
    engine.setProperty('voice', voice.id)
    engine.setProperty('rate', 150)

    # Convert the text to speech
    engine.say(text)

    # Run the engine and wait until the speech finishes
    engine.runAndWait()

def onlineAudio(text):
    # Create gTTS object
    tts = gTTS(text=text, lang=language)

    # Create a byte stream object to store the audio
    audio_file = io.BytesIO()

    # Use the write_to_fp() method to write the audio to the byte stream
    tts.write_to_fp(audio_file)

    # Set the position of the byte stream back to the beginning
    audio_file.seek(0)

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the audio from the byte stream using mixer.music.load()
    pygame.mixer.music.load(audio_file)

    # Play the audio using mixer.music.play()
    pygame.mixer.music.play()

    # Wait for the audio to finish playing before exiting the function
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

def press_ctrl_c():
    # Simulate pressing "Ctrl + C"
    keyboard.press_and_release('ctrl+c')

def clean(text):
    # Use regular expressions to remove non-alphabetic characters and spaces
    cleaned_text = text
    return cleaned_text

# Define a function to check for clipboard changes
def check_clipboard():
    clipboard_data = pyperclip.paste()
    while True:
        # Get the current clipboard data
        current_data = pyperclip.paste()

        # Check if the clipboard data has changed
        if current_data != clipboard_data:
            # Trigger the event handler
            on_clipboard_change(current_data)
            # Update the clipboard data
            clipboard_data = current_data

# Define the event handler function
def on_clipboard_change(new_data):
    if choice == "1":
        onlineAudio(clean(new_data))
    else:
        offlineAudio(clean(new_data))

# Create a separate thread for keyboard events
keyboard_thread = threading.Thread(target=keyboard.wait)
keyboard_thread.start()

# Get user input to choose text-to-speech engine
print("\033[1m" + "Note: Online audio is of better quality than offline audio." + "\033[0m")
choice = input("Enter 1 for online audio or 2 for offline audio: ")
print(f'\033[32mLeft click your mouse and hover over the text you want to hear and press "b".\033[0m')

# Register the "b" key press event listener
keyboard.add_hotkey('b', press_ctrl_c)

# Start the clipboard monitoring loop
check_clipboard()
