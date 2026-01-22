import speech_recognition as sr

def listen():
    """
    Listens to microphone input and converts it to text.
    Returns:
        str: The recognized text (lower case), or None if failed/empty.
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                # Listen for input
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                print("Recognizing...")
                
                # Recognize speech using Google Speech Recognition
                query = recognizer.recognize_google(audio, language='en-in')
                print(f"User said: {query}")
                return query.lower()
                
            except sr.WaitTimeoutError:
                print("Listening timed out.")
                return None
            except sr.UnknownValueError:
                print("Could not understand audio.")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return None
            
    except OSError as e:
        print(f"Microphone error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in STT: {e}")
        return None
