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
    browser.add_cookie({"name": "00EC7D373CB888228EE96F406DC6735174C6DC0B00CA00A5FF583B57AE52FB35CD2C4EAE311C8A9F510BCF4CF9FA781C8CADA328535DE9CCCCC2E10912D3A68C4D6477231724DD28F3BDC628CC86D02F5CE36B55A3E1811E4222977BADD2EC2FA927E76642F8A7093B1BB0353138A2F0FCA8E2DAE49FBA968EF42DD037DA47C3713B247C7837EB9BEC4DA3FEFBD0C18AE3C6E1872D1E205BCD9F1C31F2ED1C57FA39ABA7245894D0A04E1B289D4023E7CC5C822F302816915AFDB34A65E16B385AD9A8E8C85442309A9664E3C35DDFF07446C805AD6AB1C7A3CD329855B1203E45A79527AA6CC1236EF58FCFA6D318480E2E1720DC8B343ABA5348F4536E4D71F77680B9CA6F4B4843D7B97D38021881644C9CE1B7242E14D0B889BB520B9246ABC95D27A4B93104132FE4B4E04C168229CD3B7F04C6953B68C6B233EB7535894459540C7C77010CFC26E24B5140F95F013C545A6B1984BEF8DBEF378AEFC17C32", "value": "001DF223CA87D7C8771F6AB5FB14F0FAC0F03E65354703E43899496C43858F1D59043997DC1AB9D4C0473DEE4E200AE090AB636FA372F6500F105A1303E655C53AFFFDCE5D7CCC790413C3704FA707994EA5875F96541BB1B16D96FCE35F4FE7EC7199454BE0EE16D128A8989A9EBB2A26F315533695BB1EF787F2D4B5FC799298B2F76F9DD87FC15C802AAC72B1A8BFAF3FDE4A141000BBFE1536CFDD79D2890DD7177F76B029BD47250EBB2ACDAF9851588D3D6384D4AFB0B2A64650894EBDF41BAD133BA87DA9B6FD239C8819DC509415C2DC9308E5B7A15BD1EB6C5AF77211D629F0A9D19E50B45A1BEAF592FC7741DA50ED7A7E43413E50DD434B59D0B35FDDBC5261A0FA1513D9B944788916872EB84F06C9AC0C9ADD5A54B5F039F851EDF8C8B45E071E9407D1A4034C611F31943E0B9EFB5E50EE0C5995B7817176612B811F66BE7DBFAB4CBD95A4D95503C3FF41CA3DDBBEB329053A8EC8523190CB9F"})
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
