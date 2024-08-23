from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
import time
import re

load_dotenv()

class ScraperBot:
    def __init__(self, video_url):
        self.video_url = video_url
        options = Options()
        options.add_argument("headless")
        #add path to downloaded chromedriver in '.env' file
        self.driver = webdriver.Chrome(service=Service(executable_path=os.getenv('PATH_TO_DRIVER')), options=options)
    
    def createBot(self):
        self.driver.get(self.video_url)

    def closeBot(self):
        self.driver.close()

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
                    
    def exportTranscript(self, transcript, file_name):
        #write full transcript to file
        
        with open(f'{file_name}.txt', 'w') as file:
            file.write(f'Transcript (Curse words replaced with [__]):\n')
            file.write(transcript)
        
        print('Transcript exported to device.')


#TEST SCRIPTS
test = ScraperBot('https://www.youtube.com/watch?v=lFwwo0W5Ugg')
test.createBot()
video_transcript = test.scrapeTranscript()
if video_transcript:
    print(test.checkProfanity(video_transcript))
test.exportTranscript(video_transcript, 'Grading Flags')
test.closeBot()



