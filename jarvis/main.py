import sys
import os
import time
import re

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from speech.text_to_speech import speak
from speech.speech_to_text import listen
from nlp.intent_classifier import IntentClassifier
from tasks import system_tasks, web_tasks, file_tasks
from utils.time_greeting import get_greeting

def main():
    # 1. Mandatory Startup Greeting
    print("Initializing JARVIS...")
    greeting = get_greeting()
    intro_text = f"{greeting}. I am JARVIS. How can I help you today?"
    
    # Display and Speak
    print(f"\nJARVIS: {intro_text}")
    speak(intro_text)
    
    # Initialize Classifier
    classifier = IntentClassifier()
    
    # Session state
    session_data = {
        'command_count': 0,
        'last_intent': None
    }
    
    print("\n[INFO] Listening mode active. Press Ctrl+C to exit.")
    
    while True:
        try:
            # 2. Input Acquisition
            print("\nListening... (Say 'stop' or 'exit' to quit)")
            user_input = listen()
            
            # Fallback to text input
            if not user_input:
                print("Voice not detected. You can type your command below:")
                user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            print(f"Processing: {user_input}")
            session_data['command_count'] += 1
            
            # 3. Intent Classification
            intent = classifier.predict(user_input)
            response_text = ""
            
            if intent:
                tag = intent['tag']
                session_data['last_intent'] = tag
                print(f"[DEBUG] Detected Intent: {tag}")
                
                if tag == 'greeting':
                    response_text = classifier.get_response(tag)
                    
                elif tag == 'goodbye':
                    response_text = classifier.get_response(tag)
                    speak(response_text)
                    print(f"JARVIS: {response_text}")
                    break
                
                elif tag == 'help':
                    response_text = classifier.get_response(tag)
                    
                elif tag == 'time':
                    response_text = f"The current time is {system_tasks.get_time()}"
                    
                elif tag == 'date':
                    response_text = f"Today's date is {system_tasks.get_date()}"
                
                elif tag == 'time_convert':
                    # Simple extraction for "convert X minutes to seconds"
                    # This is rule-based parsing
                    try:
                        numbers = re.findall(r'\d+', user_input)
                        if numbers:
                            value = float(numbers[0])
                            unit_from = 'seconds' if 'second' in user_input else 'minutes' if 'minute' in user_input else 'hours' if 'hour' in user_input else None
                            unit_to = None
                            if 'to seconds' in user_input or 'in seconds' in user_input: unit_to = 'seconds'
                            elif 'to minutes' in user_input or 'in minutes' in user_input: unit_to = 'minutes'
                            elif 'to hours' in user_input or 'in hours' in user_input: unit_to = 'hours'
                            
                            if unit_from and unit_to:
                                response_text = system_tasks.convert_time(value, unit_from, unit_to)
                            else:
                                response_text = "I couldn't identify the units to convert."
                        else:
                            response_text = "Please specify a number to convert."
                    except Exception as e:
                        response_text = f"Error in time conversion: {e}"

                elif tag == 'wikipedia':
                    query = user_input
                    for phrase in ["wikipedia", "tell me about", "who is", "what is"]:
                        query = query.replace(phrase, "")
                    query = query.strip()
                    if query:
                        response_text = web_tasks.search_wikipedia(query)
                    else:
                        response_text = "What should I search for on Wikipedia?"
                        
                elif tag == 'open_website':
                    if "google" in user_input:
                        response_text = web_tasks.open_website("google.com")
                    elif "youtube" in user_input:
                        response_text = web_tasks.open_website("youtube.com")
                    elif "github" in user_input:
                        response_text = web_tasks.open_website("github.com")
                    elif "stackoverflow" in user_input:
                        response_text = web_tasks.open_website("stackoverflow.com")
                    else:
                        response_text = "I can open Google, YouTube, GitHub, or StackOverflow."
                
                # File Tasks
                elif tag == 'list_files':
                    response_text = file_tasks.list_files()
                    
                elif tag == 'file_create':
                    # Extract filename (simple heuristic)
                    words = user_input.split()
                    if "named" in words:
                        idx = words.index("named") + 1
                        if idx < len(words):
                            filename = words[idx]
                            response_text = file_tasks.create_file(filename, "Created by JARVIS")
                        else:
                            response_text = "Please specify a name for the file."
                    else:
                        response_text = "Please say 'create file named filename'."
                
                elif tag == 'file_delete':
                    words = user_input.split()
                    if "named" in words:
                        idx = words.index("named") + 1
                        if idx < len(words):
                            filename = words[idx]
                            # Confirmation
                            confirm = input(f"Are you sure you want to delete {filename}? (yes/no): ").lower()
                            if confirm == 'yes':
                                response_text = file_tasks.delete_file(filename)
                            else:
                                response_text = "Deletion cancelled."
                    else:
                        response_text = "Please say 'delete file named filename'."
                        
                elif tag == 'folder_create':
                    words = user_input.split()
                    if "named" in words:
                        idx = words.index("named") + 1
                        if idx < len(words):
                            folder_name = words[idx]
                            response_text = file_tasks.create_folder(folder_name)
                    else:
                        response_text = "Please say 'create folder named foldername'."
                
                # System Power
                elif tag in ['shutdown', 'restart']:
                    action = tag
                    confirm = input(f"System {action} requested. Are you sure? (yes/no): ").lower()
                    if confirm == 'yes':
                        response_text = system_tasks.system_power_control(action)
                    else:
                        response_text = "Power action cancelled."

                else:
                    response_text = classifier.get_response(tag)
                    if not response_text:
                        response_text = "I heard you, but I don't have a specific action for that yet."
            
            else:
                # Fallback / Unknown intent
                if "search" in user_input or "google" in user_input:
                     query = user_input.replace("search", "").replace("google", "").strip()
                     response_text = web_tasks.search_google(query)
                elif "notepad" in user_input:
                     response_text = system_tasks.execute_system_command("notepad")
                elif "calc" in user_input:
                     response_text = system_tasks.execute_system_command("calc")
                else:
                    response_text = "I'm sorry, I didn't understand that command."
            
            # 4. Output Response
            if response_text:
                print(f"JARVIS: {response_text}")
                speak(response_text)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()
