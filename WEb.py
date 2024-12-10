import os
import webbrowser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import logging
from bs4 import BeautifulSoup
import requests
import speech_recognition as sr

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
        
        # Fetch the website content
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text(separator=' ', strip=True)
            
            say("Should I print the content?")
            print_content = takecommand().lower()
            
            if "yes" in print_content:
                print(text_content)
                say("Here is the content.")
            else:
                say("Okay, not printing the content.")
        except Exception as e:
            logging.error(f"Error fetching the website content: {e}")
            say("There was an error fetching the content of the website.")
    else:
        logging.warning("No website name provided")
        say("Sorry, I did not get the website name.")

def get_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    say(f"The current time is {current_time}")
    logging.info(f"Current time: {current_time}")

def get_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    say(f"Today's date is {current_date}")
    logging.info(f"Current date: {current_date}")

def fill_google_form():
    say("Opening Google Form")
    logging.info("Opening Google Form")
    
    # Example of using Selenium to automate form filling
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Example URL of a Google Form (replace with actual form URL)
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSe12FGLQwrtuV7u9gopkIo94Sl8Rl9wto9yAoQtRLv51ZDlAw/viewform?usp=sf_link"
    driver.get(form_url)
    
    try:
        # Example: Finding input fields and retrieving filled content
        input_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/input')
        form_content = input_field.get_attribute('value')
        
        say(f"The form contains: {form_content}")
        logging.info(f"Google form content: {form_content}")
        
    except Exception as e:
        logging.error(f"Error reading Google form content: {e}")
        say("There was an error reading the Google form content")
    
    driver.quit()

if __name__ == '__main__':
    say('Hi, I am Jarvis')

    # Starting the logging
    logging.info('Jarvis started')

    while True:
        query = takecommand()
        if query != "None":
            if "stop" in query.lower():
                say("Stopping commands. Goodbye!")
                logging.info("Stopping commands. Goodbye!")
                break
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
            elif "google" in query.lower():
                fill_google_form()
            else:
                logging.warning(f"Unrecognized command: {query}")
                say("Sorry, I did not understand the command")
