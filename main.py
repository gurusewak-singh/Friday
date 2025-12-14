import speech_recognition as sr
import webbrowser as browser
import os
import time
import whisper
import threading
import queue
# import pyttsx3
from gtts import gTTS
import pygame 
from musicLib import music
from gemini_client import askGemini
from get_link import getlink, getsonglink

from app_control import open_system_app, close_system_app, switch_to_window, minimize_window, maximize_window, get_active_window_title, type_text
from browser_control import close_current_tab, switch_next_tab, open_new_tab, search_in_new_tab, search_in_current_tab

# initialize the mixer
pygame.mixer.init()

model = whisper.load_model("turbo")
# engine = pyttsx3.init()

# Speech Queue and Worker
speech_queue = queue.Queue()

def speech_worker():
    while True:
        task = speech_queue.get()
        if task is None:
            break
        
        task_type, content = task
        try:
            if task_type == 'text':
                # get the audio generated from text
                tts = gTTS(content)
                tts.save('temp.mp3')
                # load & play the audio
                pygame.mixer.music.load('temp.mp3')
                pygame.mixer.music.play()
                # for not exiting till the file is being played
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                # unload the temp file for deletion
                pygame.mixer.music.unload()
                # delete the temp audio file
                try:
                    os.remove('temp.mp3')
                except:
                    pass
            elif task_type == 'file':
                 pygame.mixer.music.load(content)
                 pygame.mixer.music.play()
                 while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                 # unload the temp file for deletion
                 pygame.mixer.music.unload()

        except Exception as e:
            print(f"Error in speech worker: {e}")
        finally:
            speech_queue.task_done()

# Start the worker thread
threading.Thread(target=speech_worker, daemon=True).start()

def wait_for_speech():
    speech_queue.join()

def speakmfu(filepath):
    speech_queue.put(('file', filepath))

# Creating speak function
def speak(text):
    speech_queue.put(('text', text))

def executeCommand(command):
  command = command.lower()
  # query = command.split(" ")[1]
  # if user said open then try all openning command
  if("open" in command):
      query = command.split(" ",1)[1]
      
      # Try to open as a system app first
      success, app_name = open_system_app(query)
      if success:
          speak(f"Opening {app_name}")
          return
      
      # If not found, search on web
      link = getlink(query)
      browser.open(f"{link}")
      speak(f"Openning {query}")
  
  elif "search" in command:
      query = command.split("search", 1)[1].strip()
      
      # Check for "new tab" request
      use_new_tab = False
      if query.endswith("in new tab"):
          use_new_tab = True
          query = query.replace("in new tab", "").strip()
      
      # Check for "in [browser]"
      app_name = None
      search_term = None
      
      browsers = ["chrome", "edge", "chat gpt", "copilot", "opera", "microsoft edge", "google chrome"]
      for browser_name in browsers:
          if query.endswith(f" in {browser_name}"):
              app_name = browser_name
              search_term = query[:-len(f" in {browser_name}")].strip()
              break
          elif query.endswith(f" on {browser_name}"):
              app_name = browser_name
              search_term = query[:-len(f" on {browser_name}")].strip()
              break

      if app_name:
          if not search_term:
              speak("What should I search?")
              return

          # Open/Switch to the app
          success, win_title = open_system_app(app_name)
          if success:
              speak(f"Searching {search_term} in {app_name}")
              time.sleep(0.5) # Wait for window to be active
              if use_new_tab:
                  search_in_new_tab(search_term)
              else:
                  search_in_current_tab(search_term)
          else:
              speak(f"Could not open {app_name}")
          
      else:
          # Context aware search
          active_title = get_active_window_title()
          if active_title:
              active_title = active_title.lower()
              if any(browser in active_title for browser in ["chrome", "edge", "firefox", "brave", "opera"]):
                  speak(f"Searching {query}")
                  if use_new_tab:
                      search_in_new_tab(query)
                  else:
                      search_in_current_tab(query)
                  return

          # Default fallback
          link = getlink(query)
          browser.open(f"{link}")
          speak(f"Searching {query}")

  # Browser controls
  elif "close tab" in command or "close this tab" in command:
      close_current_tab()
      speak("Closing tab")
      
  elif "switch tab" in command or "next tab" in command:
      switch_next_tab()
      speak("Switching tab")
      
  # Switch to app
  elif "switch" in command:
      query = command.split("switch", 1)[1].strip()
      if query.startswith("to "):
          query = query.split("to ", 1)[1].strip()
          
      success, win_title = switch_to_window(query)
      if success:
          # Clean title to speak only the app name (usually the last part)
          app_name = win_title
          if " - " in win_title:
              app_name = win_title.split(" - ")[-1].strip()
          
          speak(f"Switching to {app_name}")
      else:
          speak(f"Could not find window for {query}")

  elif "minimize" in command or "minimise" in command:
      keyword = "minimize" if "minimize" in command else "minimise"
      query = command.split(keyword, 1)[1].strip()
      # Optional: remove "window" or "app" if present
      query = query.replace("window", "").replace("app", "").strip()
      
      success, win_title = minimize_window(query)
      if success:
          # Clean title
          app_name = win_title
          if " - " in win_title:
              app_name = win_title.split(" - ")[-1].strip()
          speak(f"Minimizing {app_name}")
      else:
          speak(f"Could not find window for {query}")

  elif "maximize" in command:
      query = command.split("maximize", 1)[1].strip()
      # Optional: remove "window" or "app" if present
      query = query.replace("window", "").replace("app", "").strip()
      
      success, win_title = maximize_window(query)
      if success:
           # Clean title
          app_name = win_title
          if " - " in win_title:
              app_name = win_title.split(" - ")[-1].strip()
          speak(f"Maximizing {app_name}")
      else:
          speak(f"Could not find window for {query}")

  elif "new tab" in command:
      open_new_tab()
      speak("Opening new tab")

  elif "type" in command:
      query = command.split("type", 1)[1].strip()
      if query:
          type_text(query)
          speak("Done boss")
      else:
          speak("What should I type?")

  # if user said close then try to close the app
  elif "close" in command:
      query = command.split("close", 1)[1].strip()
      success, app_name = close_system_app(query)
      if success:
          speak(f"Closing {app_name}")

  # if user said play then try playing music
  elif "play" in command:
    print("triggered play")
    query = command.split("play")[1].strip()
    browser.open(getsonglink(query))
    speak(f"sure playing {query}")
  # otherwise ask gemini the querry
  else:
    speak(askGemini(command))
    pass

def process_and_execute_commands(command):
    import re
    # Separators: ' and then ', ' then ', ' and '
    # We split by these separators but keep them to check context
    parts = re.split(r'( and then | then | and )', command)
    
    final_commands = []
    current_command = parts[0].strip()
    
    # Command verbs to identify start of a new command
    command_verbs = ['open', 'close', 'play', 'search', 'switch', 'minimize', 'maximize', 'turn', 'shut', 'new tab', 'next tab', 'prev tab', 'type']
    
    for i in range(1, len(parts), 2):
        separator = parts[i]
        next_part = parts[i+1].strip()
        
        # Check if next_part starts with a verb
        is_new_command = False
        for verb in command_verbs:
            if next_part.startswith(verb):
                is_new_command = True
                break
        
        if is_new_command:
            final_commands.append(current_command)
            current_command = next_part
        else:
            # Merge back if not a new command (e.g. "search Tom and Jerry")
            current_command += separator + next_part
            
    final_commands.append(current_command)
    
    print(f"Processed commands: {final_commands}")
    
    for cmd in final_commands:
        if cmd:
            print(f"Executing: {cmd}")
            executeCommand(cmd)
            # Small delay between commands to allow UI to update
            # if len(final_commands) > 1:
            #    time.sleep(1)

def friday():
  # say initialized
  speakmfu('./mfu_mp3/initialize.mp3')
  '''obtain audio from the microphone'''
  # Initialize the recognizer (from sr)
  recognizer = sr.Recognizer()
  recognizer.energy_threshold = 5000
  recognizer.dynamic_energy_threshold = True
  
  is_active = True
  
  while 1:
    wait_for_speech()
    with sr.Microphone() as source:
        print("Say something!")
        try:
          # get audio from mic
          audio = recognizer.listen(source, timeout = 2, phrase_time_limit= 8) # timeout = 2 rakhna hai
          # recognize audio into text/string
        #   command = recognizer.recognize_google(audio).lower()
          with open("temp_audio_input.wav", "wb") as f:
              f.write(audio.get_wav_data())
          command = model.transcribe("temp_audio_input.wav")["text"].lower()
          print(command) # printing command for testing
          
          # Always listen for "shut down" to exit
          if "shut down" in command or "shutdown" in command:
            speakmfu('./mfu_mp3/shuttingdown.mp3')
            break
            
          # Always listen for "turn on" to wake up
          if "turn on" in command or "wake up" in command:
             if not is_active:
                 is_active = True
                 speakmfu('./mfu_mp3/turnon.mp3') # Or a specific "I'm back" sound
             continue

          # Only process other commands if active
          if is_active:
              if "turn off" in command or "sleep" in command:
                is_active = False
                speakmfu('./mfu_mp3/sleeping.mp3') # Or a specific "Going to sleep" sound
                continue
                
              # checking if user called friday
              elif "friday" in command:
                # Split command to check if there's a query after "friday"
                parts = command.split("friday", 1)
                query = parts[1].strip()
                
                if query:
                    # If there is a query, execute it directly
                    print(f"Direct command: {query}")
                    process_and_execute_commands(query)
                else:
                    # If just "friday", wait for command
                    speakmfu('./mfu_mp3/yesboss.mp3')
                    # get audio from mic
                    # audio = recognizer.listen(source, timeout = 2, phrase_time_limit= 12)
                    wait_for_speech()
                    audio = recognizer.listen(source, timeout = 2, phrase_time_limit= 12)
                    # recognize audio into text/string
                    # command = recognizer.recognize_google(audio)
                    with open("temp_audio_input.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                    command = model.transcribe("temp_audio_input.wav")["text"].lower()
                    print(command.lower())
                    
                    # Handle shutdown/turn off in nested loop too if needed, 
                    # but usually executeCommand handles the action.
                    # However, "turn off" inside executeCommand isn't standard.
                    # Let's just pass it to executeCommand or check here.
                    if "shut down" in command.lower() or "shutdown" in command.lower():
                        speakmfu('./mfu_mp3/shuttingdown.mp3')
                        break
                    if "turn off" in command.lower() or "sleep" in command.lower():
                        is_active = False
                        speakmfu('./mfu_mp3/sleeping.mp3')
                        continue
                        
                    process_and_execute_commands(command)
        except sr.WaitTimeoutError as w:
          pass
        except Exception as e:
          print(e)
          # Only speak error if active, to avoid annoyance when sleeping
          if is_active:
              speakmfu('./mfu_mp3/speakagain.mp3')

if __name__ == '__main__':
  # speak("Initializing Friday")
  friday()
