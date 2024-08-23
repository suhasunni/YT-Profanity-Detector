from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from dotenv import load_dotenv
import os
import time
import re

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

    def getVideoName(self):
        #WRITE
        try:
            return WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@id="above-the-fold"]'))).text
        except:
            return 'Unknown'

    def scrapeTranscript(self):
        #click 'more' button to expand description box
        more_btn = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//tp-yt-paper-button[@id="expand"]')))
        more_btn.click()
        
        #click 'show transcript' button
        try:
            show_transcript_btn = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Show transcript"]')))
            show_transcript_btn.click()
            print('Transcript Button Found!')
            
        except:
            return False
        
        #record transcript
        transcript = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, "//ytd-transcript-renderer"))).text
        
        #remove time stamps from transcript
        transcript = re.sub(r'[0-9:]', '', transcript)
        transcript = re.sub(r'\[\s__\s\]', '[__]', transcript)

        return transcript

    def checkProfanity(self, transcript):
        #check transcript for profanity
        curse_word_count = 0
        total_word_count = 0
        
        lines = transcript.split('\n')
        for line in lines:
            words = line.split(' ')
            for word in words:
                if word == '[__]':
                    curse_word_count += 1
                total_word_count +=1
        
        return round((curse_word_count/total_word_count)*100,2)  
                    
    def exportTranscript(self, transcript):
        #write full transcript to file
        #video_title = self.getVideoName()
        video_title = 'Drip Too Hard'
        
        with open(f'{video_title}.txt', 'w') as file:
            file.write(f'Transcript for {video_title}:\nAll curse words are replaced with [__].\n')
            file.write(transcript)


#TEST SCRIPTS
test = ScraperBot('https://www.youtube.com/watch?v=_YzD9KW82sk')
test.createBot()
print(test.getVideoName())
video_transcript = test.scrapeTranscript()
if video_transcript:
    test.checkProfanity(video_transcript)
test.exportTranscript(video_transcript)
test.closeBot()



