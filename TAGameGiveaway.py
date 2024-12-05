import re
from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv
import os
from pathlib import Path


#login information, configure your own .env file with login information for the TA website

env_path = Path(".env")
load_dotenv(dotenv_path=env_path)
username = os.getenv("TAUSERNAME")
password = os.getenv("TAPASSWORD")
print("gathering login information")

try:
    def run(playwright: Playwright) -> None:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.trueachievements.com/login?return=%2flogout-devices")
        print("Navigating to TrueAchievements login page")
        page.get_by_placeholder("Enter your GamerTag").click()
        page.get_by_placeholder("Enter your GamerTag").fill(username)
        print("Entering username")
        page.get_by_placeholder("Enter your password").click()
        page.get_by_placeholder("Enter your password").fill(password)
        print("Entering password")
        page.get_by_role("link", name="Log In").click()
        print("Logging in")
        page.goto("https://www.trueachievements.com/win-xbox-games")  
        print("Navigating to giveaway page")
        page.get_by_text("Click here for a chance to win").click()
        print("Entering giveaway")
        context.close()
        browser.close()


    with sync_playwright() as playwright:
        run(playwright)
        print("Giveaway entered successfully.")
except Exception as e:
    print(f"Error entering giveaway: {str(e)}")
    raise  # Re-raise the error so the workflow marks the job as failed.

    
