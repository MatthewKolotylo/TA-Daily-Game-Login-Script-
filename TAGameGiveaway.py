from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv
import os
from pathlib import Path
import smtplib
from email.message import EmailMessage


#login information, configure your own .env file with login information for the TA website

env_path = Path(".env")
load_dotenv(dotenv_path=env_path)
ta_username = os.getenv("TAUSERNAME")
ta_password = os.getenv("TAPASSWORD")
print("gathering login information")

try:
    def run(playwright: Playwright) -> None:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.trueachievements.com/login?return=%2flogout-devices")
        print("Navigating to TrueAchievements login page")
        page.get_by_placeholder("Enter your GamerTag").click()
        page.get_by_placeholder("Enter your GamerTag").fill(ta_username)
        print("Entering username")
        page.get_by_placeholder("Enter your password").click()
        page.get_by_placeholder("Enter your password").fill(ta_password)
        print("Entering password")
        page.get_by_role("link", name="Log In").click()
        print("Logging in")
        page.goto("https://www.trueachievements.com/win-xbox-games")  
        print("Navigating to giveaway page")
        page.get_by_text("Click here for a chance to win").click()
        print("Entering giveaway")
        
        #scrapping the previous winner of the giveaway, used to determine if we won yesterday's giveaway
        winner_element=page.locator('//*[@id="frm"]/div[2]/div[2]/main/div[1]/div[2]/div[2]') #previous winner element
        giveaway_winner=winner_element.inner_text().split('\n')[0] #acessing the first line of text
        
        context.close()
        browser.close()
        return giveaway_winner


    with sync_playwright() as playwright:
        giveaway_winner=run(playwright)
        print("Giveaway entered successfully.")
        print(f"Previous winner of the giveaway was: {giveaway_winner}")
        
except Exception as e:
    print(f"Error entering giveaway: {str(e)}")
    raise  # Re-raise the error so the workflow marks the job as failed.

"""The following module determines if the user has won the giveaway and then notifies the user via a email message"""
if giveaway_winner==ta_username:
    #587 is the port number for the server for gmail account
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    #sender account email and password
    gmail_username=os.getenv("GMAILUSERNAME")
    gmail_password=os.getenv("GMAILPASSWORD") #make app password, lets you use gmail with 3rd party applications like this one

    server.login(gmail_username,gmail_password) 

    def send_email(subject, body, sender, reciever):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = reciever
        msg.set_content(body)
        server.send_message(msg)
        print("Email sent!")

    #email varriables
    subject="You have won the TrueAchievements giveaway!"
    body="Well played! this program turned out to be usefull and as such won the TA giveaway.\n Thank your past self for setting up your future."
    sender=gmail_username
    reciever=os.getenv("MYEMAIL")

    send_email(subject, body, sender, reciever)


    
