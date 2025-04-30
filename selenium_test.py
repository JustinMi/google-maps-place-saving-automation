import csv
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CHROME_PROFILE_PATH = os.path.expanduser("~/Library/Application Support/Google/Chrome")
PROFILE_DIRECTORY = "Default"
CSV_FILE_PATH = "Takeout/Saved/Favorite places.csv"

def initialize_webdriver(profile_path: str, profile_directory: str) -> uc.Chrome:
    """
    Initialize the WebDriver with an existing Chrome profile using undetected-chromedriver
    """
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_path}")  # Use existing Chrome profile
    options.add_argument(f"--profile-directory={profile_directory}")  # Specify the profile directory
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    # options.add_argument("--remote-debugging-port=9222")
    options.debugger_address = "127.0.0.1:9222"

    print("Using Chrome profile: " + profile_path)
    print("Using profile directory: " + profile_directory)
    print(uc.__version__)

    # Initialize the undetected ChromeDriver
    driver = uc.Chrome(options=options)

    print("WebDriver initialized with the specified profile.")

    return driver

def save_to_favorites(driver, title: str, url: str, note: str = None):
    """
    Save a location to Favorites on Google Maps and optionally add a note.

    Args:
        driver: The WebDriver instance.
        url: The URL of the location to save.
        note: The optional note to add to the location.
    """
    print("*" * 50)
    print(f"Saving '{title}' to Favorites...")

    # Open a webpage
    driver.get(url)
    print(f"Navigated to URL: {url}")

    # Click the "Save" button
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Save"][data-value="Save"]'))
    )
    save_button.click()
    print("Clicked the Save button.")

    # Click the "Favorites" button
    favorites_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-checked="false"].MMWRwe.fxNQSd'))
    )
    favorites_button.click()
    print("Clicked the Favorites button.")

    if note:
        # Handle the intercepting element
        intercepting_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.EoqU6d'))
        )
        intercepting_element.click()
        print("Clicked the intercepting element.")

        # Expand Favorites details section
        favorites_details_dropdown_carrot = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Show place lists details"][data-value="Show place lists details"]'))
        )
        favorites_details_dropdown_carrot.click()
        print("Clicked the Favorites details dropdown.")

        # Open the "Add Note" modal
        add_note_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Add note in Favorites"]'))
        )
        add_note_button.click()
        print("Opened Add Note modal.")

        time.sleep(3)  # gimme a sec to react

        # Enter text into the selected text box
        active_element = driver.switch_to.active_element  # Get the currently selected (active) element
        active_element.send_keys(note)
        print(f"Entered text: {note}")

        # Click the "Done" button
        done_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.okDpye.PpaGLb.mta2Ab'))
        )
        done_button.click()
        print("Clicked the 'Done' button.")

# Initialize the WebDriver
print("Initializing WebDriver with Chrome profile...")
driver = initialize_webdriver(CHROME_PROFILE_PATH, PROFILE_DIRECTORY)
print("WebDriver initialized with Chrome profile: " + CHROME_PROFILE_PATH)

# Open the CSV file and read it line by line
with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)  # Use DictReader to access columns by name
    for row in csv_reader:
        # Extract data from the current row
        title = row["Title"]
        note = row["Note"]
        url = row["URL"]

        # Print the contents of the current row
        save_to_favorites(driver, title, url, note)

# Close the browser
driver.quit()
