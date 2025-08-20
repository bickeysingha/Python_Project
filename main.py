import speech_recognition as sr
import webbrowser
import pyttsx3 as pt
import musiclibrary
import requests

from openai import OpenAI






newsapi = "18c1d62158484db6b1426477ccb05940"

recognizer = sr.Recognizer()

def speak(c):
    eng = pt.init()
    eng.setProperty('rate', 145)
    eng.say(c)
    eng.runAndWait()

def aiprocess(command):
    client = OpenAI(    api_key="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")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

def processcommand(c):
    if "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, song not found in music library.")
    elif c.lower().startswith("news"):
        url = f"https://newsapi.org/v2/everything?q=apple&from=2025-08-17&to=2025-08-17&sortBy=popularity&apiKey={newsapi}"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            print("Top Apple Headlines on 2025-08-17:\n")
            for i, article in enumerate(articles[:5], start=1):
                print(f"{i}. {article['title']}")
                speak(article['title'])
        else:
            speak("Failed to fetch news.")
    else:
        response = aiprocess(c)
        speak(response)

if __name__ == "__main__":
    speak("Initializing Marco....")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening!")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
            print("Recognizing...")
            word = recognizer.recognize_google(audio)
            print(word)

            if word.lower() == "hello":
                speak("Yo man")
                with sr.Microphone() as source:
                    speak("Give command")
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                command = recognizer.recognize_google(audio)
                processcommand(command)

        except Exception as e:
            print(f"Error: {e}")
