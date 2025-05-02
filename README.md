# Google Maps Place Saving Automation

This project automates the process of saving a list of places from a CSV file (generated from Google Takeout) to Google Maps using Selenium and `undetected-chromedriver`.

## Prerequisites

1. **Python**: Ensure you have Python 3.7 or higher installed.
2. **Google Chrome**: Install the latest version of Google Chrome.
3. **Chrome Extensions**:
   - Install an ad blocker extension (e.g., [uBlock Origin](https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm)) to prevent pop-ups or ads from interfering with the automation.

## Dependencies

Install the required Python packages using `pip`:

```bash
pip install selenium undetected-chromedriver
```

## How to Run the Script

### Prepare Your CSV File:
1. Download maps data from Google Takeout: https://takeout.google.com.
2. If you don't have data to download, then just structure your CSV to have the following columns:
   - **Title**: The name of the location.
   - **Note**: (Optional) A note to add to the location.
   - **URL**: The Google Maps URL of the location.

### Set Up Chrome Profile:
1. Ensure you have a Chrome profile set up with the required extensions (e.g., ad blocker).
2. Update the `CHROME_PROFILE_PATH` and `PROFILE_DIRECTORY` variables in the script to point to your Chrome profile directory. By default, the script uses:
   ```python
   CHROME_PROFILE_PATH = "~/Library/Application Support/Google/Chrome"
   PROFILE_DIRECTORY = "Default"

### Set the right constants

- Set the LIST_NAME variable in the script to the desired Google Maps category (e.g., "Alps driving roads"). This saved list must already exist in your Google Maps.
- Set the LIST_INDEX to the index of the list in the "save location" dropdown. It's 0-indexed.
- Set CHROME_PROFILE_PATH to the path of your Chrome profile.
- Set CHROME_PROFILE_DIRECTORY to the name of your Chrome profile directory.
- Set CSV_FILE_PATH to the path of your CSV file.

### Run the Script:
Execute the script using Python:
thon selenium_test.py

```bash
python3 selenium_test.py
```

## Error Logging:
If any errors occur during the process, they will be logged in the `error_log.txt` file.

## Notes:
- The script uses undetected-chromedriver to bypass bot detection mechanisms on Google Maps.
- Ensure your Chrome browser is not running when the script starts, as it will attach to the specified Chrome profile.
- The script includes a delay (`time.sleep`) to handle animations or transitions on the Google Maps interface. You can try to remove it if you want.
