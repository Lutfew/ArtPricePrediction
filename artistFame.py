from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, SessionNotCreatedException
import pandas as pd
import time
import unicodedata

# Global Variables
driver = None
artists_data = pd.DataFrame()
unique_artists = {}

def clean_string(text):
    nfkd_string = unicodedata.normalize("NFKD", str(text))
    return "".join([c for c in nfkd_string if not unicodedata.combining(c)])

def start_driver():
    options = Options()
    options.headless = False  # Change to True for headless mode
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(10)  # Implicit wait time
    except SessionNotCreatedException:
        raise Exception("Driver could not be started. Please check your Chrome installation and WebDriver.")
    return driver

def artsy_link(artist):
    clean_name = clean_string(artist)
    url = f"https://artsy.net/artist/{'-'.join(clean_name.lower().split())}"
    return url

def biography_artsy(artist):
    try:
        driver.get(artsy_link(artist))
        time.sleep(2)  # Waiting for the page to load properly
        biography = driver.find_element("xpath", "//div[@class='ReadMore__Container-sc-1bqy0ya-0 hSZzlP']").text
        return biography
    except NoSuchElementException:
        print(f"Biography not found for {artist}")
        return ""

def generate_artist_fame():
    artists = artists_data['artist'].tolist()
    artists_fame = []
    for artist in artists:
        biography = biography_artsy(artist)
        fame = len(biography.split())
        artists_fame.append(fame)
    artists_data['fame'] = artists_fame
    artists_data.to_csv("artistFame.csv", index=False)

def main():
    global driver, artists_data
    artists_data = pd.read_csv("https://raw.githubusercontent.com/Lutfew/ArtPricePrediction/main/cleanedArtDataset.csv")
    driver = start_driver()
    generate_artist_fame()
    driver.quit()

if __name__ == "__main__":
    main()