import speech_recognition as sr
import os
import webbrowser
from openai import OpenAI
from config import apikey
from config import newsApi
import datetime
import json
import random
import requests

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=apikey,
)

chatStr = ""

def chat(query):
    global chatStr
    chatStr += f"Harry: {query}\n Jarvis: "
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": chatStr}
        ],
        model="gpt-4o"
    )

    # Correct response parsing
    say(response.choices[0].message.content.strip())
    chatStr += f"{response.choices[0].message.content.strip()}\n"
    return response.choices[0].message.content.strip()

def get_news(genre, country):
    url = f'https://newsdata.io/api/1/news?apikey={newsApi}&category={genre}&country={country}'
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error: Unable to fetch news (status code: {response.status_code})"

    news_data = response.json()

    if news_data['status'] != 'success':
        return f"Error: {news_data.get('message', 'Unknown error')}"

    articles = news_data.get('results', [])
    top_news = articles[:5]

    news_text = f"Top 5 news in {genre} genre for {country}:\n"
    for idx, article in enumerate(top_news, 1):
        news_text += f"{idx}. {article['title']}\n"
        news_text += f"   Source: {article['source_id']}\n"
        news_text += f"   {article['link']}\n\n"

    return news_text

def provide_news(genre, country):
    news = get_news(genre, country)
    print(news)
    say(news)

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

    # with open(f"Openai/prompt-{random.randint(1, 123456789)}", "w") as f:
    #     f.write(text)
    #     print("File created")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
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
        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        # open messages
        elif "open messages".lower() in query.lower():
            os.system(f"open /System/Applications/Messages.app")

        # Add a feature to play a specific song

        # Add a feature to display weather

        # Add a feature to display news

        # feature to get an email written out
        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
            say("Done sir, please let me know if there is anything else")

        elif "Jarvis Quit".lower() in query.lower():
            exit()

        elif "Reset Chat".lower() in query.lower():
            chatStr = ""

            # Provide news based on genre and country
        elif "news" in query.lower():
            say("Please tell me the genre of news you are interested in.")
            genre = takeCommand()
            say("Please tell me the country code for the news.")
            country = takeCommand()
            news = get_news(genre, country)
            say(news)

        else:
            print("Chatting.......")
            chat(query)
