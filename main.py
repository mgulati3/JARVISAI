import speech_recognition as sr
import os
import webbrowser
from openai import OpenAI
from config import apikey
import datetime
import json
import random

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=apikey,
)

# openai.api_key = apikey

def ai(prompt):
    text = f"OpenAI response for prompt: {prompt} \n *********************** \n\n"

    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o"
    )

    # Correct response parsing
    text += response.choices[0].message.content.strip()

    print(text)

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/prompt-{random.randint(1, 123456789)}", "w") as f:
        f.write(text)
        print("File created")



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
        if "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
