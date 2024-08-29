from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
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



#User Interaction
response = input('Enter video URL: ')
bot = ScraperBot(response)
bot.createBot()
transcript = bot.scrapeTranscript()
path = input('What would you like to do?\n(1) Get Profanity Score\n(2) Export Video Transcript\n')
if path == '1':
    print('The percentage of curse words in this video is ' + str(bot.checkProfanity(transcript)) + '%.')
else:
    video_name = input('Enter Video Name:')
    bot.exportTranscript(transcript, video_name)
bot.closeBot()