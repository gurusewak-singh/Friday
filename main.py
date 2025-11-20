import speech_recognition as sr
import webbrowser as browser
import os
from gtts import gTTS
import pygame 
from musicLib import music
from gemini_client import askGemini

# Creating peak function
def speak(text):
  # initialize the mixer
  pygame.mixer.init()
  # get the audio generated from text
  tts = gTTS(text)
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
  os.remove('temp.mp3')

def executeCommand(command):
  command = command.lower()
  # if user said open then try all openning command
  if("open" in command):
    if "google" in command:
      browser.open("https://google.com")
      speak("Opening google")
    elif "youtube" in command:
      browser.open("https://youtube.com")
      speak("Openning youtube")
    elif "linkedin" in command:
      browser.open("https://linkedin.com")
      speak("Openning Linkedin")
    elif "github" in command:
      browser.open("https://github.com")
      speak("Openning github")
  # if user said play then try playing music
  elif "play" in command:
    print("triggered play")
    browser.open(music[command.split(" ")[1]])
    speak(f"Playing {command.split(" ")[1]}")
  # otherwise ask gemini the querry
  else:
    speak(askGemini(command))
    pass

if __name__ == '__main__':
  # say initialized
  speak("Friday Initialized!!")
  '''obtain audio from the microphone'''
  # Initialize the recognizer (from sr)
  recognizer = sr.Recognizer()
  # recognizer.energy_threshold = 4000
  # recognizer.dynamic_energy_threshold = True
  while 1:
    with sr.Microphone() as source:
        print("Say something!")
        try:
          # get audio from mic
          audio = recognizer.listen(source, timeout = 2, phrase_time_limit= 5) # timeout = 2 rakhna hai
          # recognize audio into text/string
          command = recognizer.recognize_google(audio).lower()
          print(command) # printing command for testing
          if "turn off" in command:
            break
          # checking if user called friday
          elif "friday" in command:
            speak("Yes boss")
            # get audio from mic
            audio = recognizer.listen(source, timeout = 2, phrase_time_limit= 5)
            # recognize audio into text/string
            command = recognizer.recognize_google(audio)
            print(command.lower())
            if "turn off" in command.lower():
              speak("Turning off")
              break
            executeCommand(command)
        except sr.WaitTimeoutError as w:
          pass
        except Exception as e:
          print(e)
          speak("Please speak again! I couldn't understand")