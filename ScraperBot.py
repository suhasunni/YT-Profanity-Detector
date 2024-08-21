from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
import time

load_dotenv()

class ScraperBot:
    def __init__(self, video_url):
        self.video_url = video_url
        self.driver = webdriver.Chrome(service=Service(executable_path=os.getenv('PATH_TO_DRIVER')))

    
    def makeBot(self):
        self.driver.get(self.video_url)
        time.sleep(100)
        self.driver.close()

test = ScraperBot('https://www.google.com/')
test.makeBot()


