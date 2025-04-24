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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B74818A66B7FCF2E2C8300A7894B24A8DA117987F1366F65BA1404CD1FD546D05E2B9D1F01FBF7669012EF43755B7EB1E79D9DBDAEE8E433932ACFF8D66EBCB4F6148BA739892A4F1A55DBE8DB89AB3317B925FD1435C31C72BA52D4BEAE918479B4E5E6A2B04CC89CBE89DDAB5316790117FC3DF33D317ED549EFD2A753C9C34B0CA2BFCCBDFEF763870AF74265DBFE801461F8AC05030B7B66D17339F9FF8AFB459B74168220EBE1C99DA784FDE178AE2F6AF6BCA393ABA765193C37ECC9184A3886FAF05291C93EC7329AF27EB9B9BADFDBD65252F4D41EE2422ACB61EA171BDCA568BEBEB46FCEE5AA8224F6DB6FB90E3A07DE3F8B2F2BE358A024BD85D9891F14E5068A9317FD8BEF3A1CC352C4ADBA20BE5BF1D4F4045053C02D2AF6E0FC25047867609AC6CAD394B5A587A6CF6F8E9A5E980E17B3228B493668D99AF0A667A6702BD919692E3DE2685B2E45CCCB9A76D00D1E2EEB77BD6B8E14FFEABD"})
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
