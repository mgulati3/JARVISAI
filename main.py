import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import json

openai.api_key = apikey



def ai(prompt):
    text = f"Openai response for prompt: {prompt} \n *********************** \n\n"

    response = openai.ChatCompletion.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-4o"
    )

    # Correct response parsing
    response_text = response['choices'][0]['message']['content']
    text += response_text

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/prompt-{random.randint(1, 123456789)}.txt", "w") as f:
        f.write(text)


def say(text):
    os.system(f"say {text}")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing......")
            query = r.recognize_google(audio, language='en-US')
            print(f"User said: {query}")
            return query
        except Exception as e:
            return " Some error Occurred. Sorry from Jarvis"


if __name__ == '__main__':
    print('PyCharm')
    say("Hello I am Jarvis A.I")
    while True:
        print("Listening.......")

        # todo: add more sites
        # opening sites
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ["instagram", "https://www.instagram.com"],
                 ["github", "https://www.github.com"], ["spotify", "https://www.spotify.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir......")
                webbrowser.open(site[1])
        # say(query)
        if "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir the time is {strfTime}")

        # open facetime
        if "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        # open messages
        if "open messages".lower() in query.lower():
            os.system(f"open /System/Applications/Messages.app")

        # Add a feature to play a specific song

        # feature to get an email written out
        if "using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
