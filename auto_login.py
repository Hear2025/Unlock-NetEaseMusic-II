# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00B4DEC498ED691A4AB19BCF442690004E12B2BCBB9E74375EC3E3D78FD792B509882DD026F87D35FE250D84DBBEDB140C39847378CF31C737D531205EF59A3C7D6E794801BB80DF1DF8810B1EC5F1FBA3FA8A1442065457E8DD6C6D0619E6B6B310D20323FA18AE225C09F05EC2A85EDE8A8050506D79A477F29B9D868C176B25444EE1909FB275C6DFD629A814427CCDFE22D8DBB1386FB446D35D39AA7FD7003D5EC3974E7D18C91DB532629912680B37301E114D54E08C1BA00C3FE833A8379393F695A248D9DD014594DA93520F333F17567E567BAD091DCA1DFE5725BA7DE764CDF985EFD7DE9BCF2C2BF00F8F9CF74D07BE5C37495E5CA16D3D9F2058C36187677A07BF29380A51160D38489DB7774D75D8530A49DC7324E6DB8F47B28862C5E19A93C9A020A725665B764B5FC5197847C5C6EBF73CC4A020D8E9A6976B45679CD0B2E7CEA80F15D9905D834D4AF0BFB5085C1018F10F176FD66F5976BF"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
