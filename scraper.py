from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
import time


load_dotenv()
driver_path = os.getenv('PATH_TO_DRIVER')
website = 'https://www.youtube.com/@MrBeast'
print(driver_path)
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)


def makeBot():
    driver.get(website)
    time.sleep(10)
    driver.close()

makeBot()

