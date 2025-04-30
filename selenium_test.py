import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


CHROME_PROFILE_PATH = os.path.expanduser("~/Library/Application Support/Google/Chrome")
PROFILE_DIRECTORY = "Default"

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

# Initialize the WebDriver
print("Initializing WebDriver with Chrome profile...")
driver = initialize_webdriver(CHROME_PROFILE_PATH, PROFILE_DIRECTORY)
print("WebDriver initialized with Chrome profile: " + CHROME_PROFILE_PATH)

# Open a webpage
driver.get("https://www.google.com/maps/place/Erge+Chicken+Rice+Noodles/data=!4m2!3m1!1s0x3720ca6aafeeae0f:0xea6df3e75ae9148c")

# Click the "Save" button
save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Save"][data-value="Save"]')))
save_button.click()
print("Clicked the Save button.")

# Click the "Favorites" button
favorites_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-checked="false"].MMWRwe.fxNQSd')))
favorites_button.click()
print("Clicked the Favorites button.")

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
print("Opened Add Note modal.")

# Close the browser
driver.quit()
