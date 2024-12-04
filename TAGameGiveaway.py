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


try:
    def run(playwright: Playwright) -> None:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.trueachievements.com/login?return=%2flogout-devices")
        page.get_by_placeholder("Enter your GamerTag").click()
        page.get_by_placeholder("Enter your GamerTag").fill(username)
        page.get_by_placeholder("Enter your password").click()
        page.get_by_placeholder("Enter your password").fill(password)
        page.get_by_role("link", name="Log In").click()
        page.goto("https://www.trueachievements.com/win-xbox-games")  
        page.get_by_text("Click here for a chance to win").click()
        context.close()
        browser.close()


    with sync_playwright() as playwright:
        run(playwright)
except Exception as e:
    print("Script can only be run once a day, you have already entered the giveaway today.")
