import speech_recognition as sr
import os
import webbrowser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import threading
import logging

# Configure logging
logging.basicConfig(filename='jarvis.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def say(text):
    logging.info(f'Speaking: {text}')
    os.system(f'say "{text}"')

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 2
        logging.info("Listening...")
        print("Listening...")
        audio = r.listen(source)
        logging.info("Finished listening...")

        try:
            logging.info("Recognizing...")
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            logging.info(f"User said: {query}")
            print(f"User said: {query}\n")
            say(query)
            return query
        except sr.UnknownValueError:
            logging.error("Speech recognition could not understand audio")
            print("Sorry, I did not get that")
            say("Sorry, I did not get that")
            return "None"
        except sr.RequestError:
            logging.error("Could not request results from Google Speech Recognition service")
            print("Sorry, my speech service is down")
            say("Sorry, my speech service is down")
            return "None"

def get_time():
    current_time = datetime.now().strftime("%I:%M %p")
    logging.info(f"The current time is {current_time}")
    say(f"The current time is {current_time}")

def get_date():
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    logging.info(f"Today's date is {current_date}")
    say(f"Today's date is {current_date}")

# Predefined site URLs
site_urls = {
    "youtube": "https://www.youtube.com/",
    "google": "https://www.google.com/",
    "spotify": "https://www.spotify.com/",
    "codeforces": "https://www.codeforces.com/"
}

def get_website_url(site_name):
    """
    Function to get the URL of a given site.
    If the site is in the predefined list, return the URL.
    Otherwise, construct a URL using a standard pattern.
    """
    site_name_cleaned = site_name.replace(" ", "")
    if site_name_cleaned in site_urls:
        return site_urls[site_name_cleaned]
    else:
        return f"https://www.{site_name_cleaned}.com/"

def ask_for_website_name():
    say("Please tell me the name of the website.")
    site_name = takecommand()
    if site_name and site_name != "None":
        url = get_website_url(site_name)
        say(f"Opening {site_name}")
        logging.info(f"Opening {site_name}: {url}")
        webbrowser.open(url)
    else:
        logging.warning("No website name provided")
        say("Sorry, I did not get the website name.")

if __name__ == '__main__':
    say('Hi, I am Hitler')
    
    # Starting the logging
    logging.info('Jarvis started')
    print('VS CODE')

    while True:
        query = takecommand()
        if query != "None":
            if "stop" in query.lower():
                say("Stopping commands. Goodbye!")
                logging.info("Stopping commands. Goodbye!")
                break
            elif "spotify" in query.lower():
                play_music()
            elif "play music" in query.lower():
                play_music()
            elif "what is the time" in query.lower() or "current time" in query.lower():
                get_time()
            elif "what is the date" in query.lower() or "current date" in query.lower():
                get_date()
            elif "facetime" in query.lower():
                logging.info("Facetime functionality not implemented yet")
                say("Sorry, the FaceTime functionality is not implemented yet")
            elif "chrome history" in query.lower():
                logging.info("Opening Chrome history")
                say("Opening Chrome history")
                webbrowser.open("chrome://history/")
            elif "search website" in query.lower():
                ask_for_website_name()
            else:
                for site in site_urls:
                    if f"open {site}" in query.lower():
                        say(f"Opening {site} sir")
                        logging.info(f"Opening {site}")
                        webbrowser.open(site_urls[site])
                        break
                else:
                    logging.warning(f"Unrecognized command: {query}")
                    say("Sorry, I did not understand the command")