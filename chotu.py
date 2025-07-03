import sounddevice as sd
import wavio
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import os
import sys
import webbrowser
import random

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    print("CHOTU:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    fs = 16000
    duration = 5
    talk("Listening. Please speak now.")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        wavio.write("recording.wav", recording, fs, sampwidth=2)
    except Exception as e:
        talk(f"Recording failed: {e}")
        return ""

    r = sr.Recognizer()
    try:
        with sr.AudioFile("recording.wav") as source:
            audio_data = r.record(source)
            command = r.recognize_google(audio_data, language='en-in').lower()
            print("You said:", command)
            return command
    except sr.UnknownValueError:
        talk("Sorry, I didn’t catch that.")
    except sr.RequestError:
        talk("There was a network issue while connecting to Google.")
    return ""

def tell_silly_joke():
    jokes = [
        "Why did the computer catch a cold? Because it left its Windows open.",
        "Why don't scientists trust atoms? Because they make up everything.",
        "Why did the tomato turn red? Because it saw the salad dressing.",
        "Why did the student eat his homework? Because the teacher said it was a piece of cake.",
        "What do you call a bear with no teeth? A gummy bear.",
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "What did one wall say to the other? I’ll meet you at the corner.",
        "What’s brown and sticky? A stick.",
        "Why can't your nose be 12 inches long? Because then it would be a foot.",
        "I told my computer I needed a break, and it said no problem—it'll crash!"
    ]
    joke = random.choice(jokes)
    talk(joke)

def run_chotu():
    command = take_command()
    print("DEBUG: Command received ->", command)

    if "hello chotu" in command or "hi" in command:
        talk("Hi Tulasi, how can I help you?")

    elif "play" in command:
        song = command.replace("play", "").strip()
        talk(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)

    elif "search" in command:
        query = command.replace("search", "").strip()
        talk(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "time" in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The time is {time}")

    elif "weather" in command or "climate" in command:
        city = command.replace("what's the weather in", "").replace("climate", "").strip()
        if city:
            url = f"https://www.google.com/search?q=weather+in+{city}"
            talk(f"Getting weather for {city}")
        else:
            url = "https://www.google.com/search?q=current+weather"
            talk("Getting current weather")
        webbrowser.open(url)

    elif "who is" in command or "what is" in command:
        topic = command.replace("who is", "").replace("what is", "").strip()
        try:
            info = wikipedia.summary(topic, sentences=2)
            talk(info)
        except:
            talk("Sorry, I couldn't find information about that.")

    elif "joke" in command:
        tell_silly_joke()

    elif "open chrome" in command:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            talk("Opening Google Chrome")
            os.startfile(chrome_path)
        else:
            talk("Chrome path not found")

    elif "open google" in command:
        talk("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        talk("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open code" in command or "open vs code" in command:
        talk("Opening Visual Studio Code")
        os.system("code")

    elif "exit" in command or "stop" in command:
        talk("Take care of your health and have a nice day. Goodbye.")
        sys.exit()

    elif command != "":
        try:
            info = wikipedia.summary(command, sentences=1)
            talk(info)
        except:
            talk("I heard you, but I am still learning that command.")

# Start CHOTU
talk("Hi, I am CHOTU, your personal voice assistant. I am here to help you.")
while True:
    run_chotu()