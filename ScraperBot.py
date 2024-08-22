from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from dotenv import load_dotenv
import os
import time

load_dotenv()

class ScraperBot:
    def __init__(self, video_url):
        self.video_url = video_url
        #add path to downloaded chromedriver in '.env' file
        self.driver = webdriver.Chrome(service=Service(executable_path=os.getenv('PATH_TO_DRIVER')))
    
    def createBot(self):
        self.driver.get(self.video_url)

    def closeBot(self):
        self.driver.close()

    def scrapeTranscript(self):
        #click 'more' button to expand description box
        more_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//tp-yt-paper-button[@id="expand"]')))
        more_btn.click()
        
        #click 'show transcript' button
        show_transcript_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Show transcript"]')))
        show_transcript_btn.click()
        print('The button worked!', show_transcript_btn.text)
        time.sleep(10)


test = ScraperBot('https://www.youtube.com/watch?v=cZYNADOHhVY')
test.createBot()
test.scrapeTranscript()
test.closeBot()



