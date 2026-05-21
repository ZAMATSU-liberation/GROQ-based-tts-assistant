import speech_recognition as sr
import webbrowser
import edge_tts
import time
import requests
from groq import Groq
import pygame
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()


recognizer = sr.Recognizer()
#________________________________________________________________________________________
VOICE = "en-GB-ThomasNeural"
async def _speak(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save('temp.mp3')

def speak(text):
    asyncio.run(_speak(text))
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.music.unload()
    os.remove('temp.mp3') # this will remove the temp file after playing the audio so it wont take space 

def aiProcess(command):
    client = Groq(
        api_key=os.getenv("API_KEY") #load from .env file by os.getenv
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": command # the command ordered by user will be sent here and initalize response from model
            }
        ]
    )

    return response.choices[0].message.content 


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        speak("opening google hold on sir..")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
        speak("opening linkedin hold on sir..")

    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")
        speak("Nigga stop using this racist app!!")

    elif c.lower().startswith("play"):
        word = c.lower().replace("play","").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={word}")
        speak(f"playing {word}on youtube hold on sir..")
    elif "news" in c.lower():
        speak("You need to add a news API or use Groq for headlines.")
    elif "time"in c.lower():
        current_time = time.strftime("%I:%M %p")
        speak(f"the current time according to your ST is {current_time}")
    elif f"search {word}" in c.lower():
        webbrowser.open(f"https://search.brave.com/search?q={word}&summary=1&conversation=091c858610f44c9a4024cffb49920b187941")
        speak(f"hold on im searching {word} on internet")
    else:
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
     speak("Jarvis active...")
     while True:
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)

            word = r.recognize_google(audio)
            print(f"you said:{word}")   
            wake_words = ["jarvis","buddy","hey"]
            if any(wake_word in word.lower() for wake_word in wake_words):
                speak("Yes boss, how can I help you?")
    
            
                with sr.Microphone() as source: # gonna recognize the command after wake word and initialize the query 
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

            

        except Exception as e:
            print(f"Error: {e}")
