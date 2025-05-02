import csv
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

CATEGORY = "Alps driving roads" # Change this to the desired category. It needs to already exist in your Google Maps.
DATA_INDEX = 4 # Change this to the index of the category in the list of categories. It's 0-indexed.
CHROME_PROFILE_PATH = os.path.expanduser("~/Library/Application Support/Google/Chrome")
PROFILE_DIRECTORY = "Default"
CSV_FILE_PATH = f"Takeout/Saved/{CATEGORY}.csv"


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
    options.debugger_address = "127.0.0.1:9222"

    print("Using Chrome profile: " + profile_path)
    print("Using profile directory: " + profile_directory)
    print(uc.__version__)

    # Initialize the undetected ChromeDriver
    driver = uc.Chrome(options=options)

    print("WebDriver initialized with the specified profile.")

    return driver

def log_error(action: str, title: str, url: str):
    """
    Log an error message to a file if the save button is not found.

    Args:
        action: A string description of the action that caused the error.
        title: The title of the location.
        url: The URL of the location.
    """
    print("Error. Skipping.")
        
    # Print failed items to a file
    with open("error_log.txt", "a") as error_file:
        error_file.write(f"Error for {title} at {url} while doing {action}\n")

def save_to_category(driver, category: str, title: str, url: str, note: str = None):
    """
    Save a location to a category on Google Maps and optionally add a note.

    Args:
        driver: The WebDriver instance.
        category: The category to save the location under.
        title: The title of the location.
        url: The URL of the location to save.
        note: The optional note to add to the location.
    """
    print("*" * 50)
    print(f"Saving '{title}' to {category}...")

    # Open a webpage
    try:
        print(f"Navigating to URL: {url}")
        driver.get(url)
        print(f"Navigated to URL: {url}")
    except Exception as e:
        log_error("navigating to URL", title, url)
        return

    # Click the "Save" button
    try:
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Save"][data-value="Save"]'))
        )
        save_button.click()
        print("Clicked the Save button.")
    except TimeoutException:
        log_error("clicking Save button", title, url)
        return

    # Click the category button
    try:
        category_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'div[aria-checked="false"].MMWRwe.fxNQSd[data-index="{DATA_INDEX}"]'))
        )
        category_button.click()
        print(f"Clicked the {category} button.")
    except TimeoutException:
        log_error(f"clicking {category} button", title, url)
        return

    # Wait for the "Saved" confirmation message
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Saved"][data-value="Saved"]'))
        )
        print("Saved.")
    except TimeoutException:
        log_error("waiting for Saved confirmation", title, url)
        return

    if note:
        # Handle the intercepting element if it exists
        try:
            intercepting_element = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.EoqU6d'))
            )
            intercepting_element.click()
            print("Clicked the intercepting element.")
        except TimeoutException:
            print("Intercepting element did not appear. Proceeding without clicking it.")

        # Expand the category's details section
        try:
            want_to_go_details_dropdown_carrot = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Show place lists details"][data-value="Show place lists details"]'))
            )
            want_to_go_details_dropdown_carrot.click()
            print(f"Clicked the {category} details dropdown.")
        except TimeoutException:
            log_error(f"expanding {category} details dropdown", title, url)
            return

        # Open the "Add Note" modal
        try:
            add_note_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'button[aria-label="Add note in {category}"]'))
            )
            add_note_button.click()
            print("Opened Add Note modal.")
        except TimeoutException:
            log_error("clicking Add Note button", title, url)
            return

        time.sleep(0.5)  # gimme a sec to react

        # Enter text into the selected text box
        try:
            active_element = driver.switch_to.active_element  # Get the currently selected (active) element
            active_element.send_keys(note)
            print(f"Entered text: {note}")
        except Exception as e:
            log_error(f"entering text {e} into note box", title, url)
            return

        # Click the "Done" button
        try:
            done_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.okDpye.PpaGLb.mta2Ab'))
            )
            done_button.click()
            print("Clicked the 'Done' button.")
        except TimeoutException:
            log_error("clicking 'Done' button", title, url)
            return

        # Wait for Edit Note to be clickable, indicating the note was saved
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'button[aria-label="Edit note in {category}"]'))
            )
            print("Note saved.")
        except TimeoutException:
            log_error("waiting for Edit Note button (saving note)", title, url)
            return

    time.sleep(0.5) # Pause to allow for any animations or transitions

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
        save_to_category(driver, CATEGORY, title, url, note)

# Close the browser
driver.quit()
