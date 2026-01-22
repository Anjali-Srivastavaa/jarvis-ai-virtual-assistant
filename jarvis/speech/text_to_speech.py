import pyttsx3

# Initialize the engine once
try:
    engine = pyttsx3.init()
    # Optional: Set properties (rate, volume, voice)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
except Exception as e:
    print(f"Error initializing TTS engine: {e}")
    engine = None

def speak(text):
    """
    Converts text to speech using pyttsx3.
    Args:
        text (str): The text to speak.
    """
    if not engine:
        print("TTS Engine not available.")
        print(f"System says: {text}")
        return

    try:
        print(f"JARVIS: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in TTS: {e}")
