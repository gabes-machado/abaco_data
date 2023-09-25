from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def driversetup():
    options = webdriver.ChromeOptions()
    # run Selenium in headless mode
    
    # overcome limited resource problems
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("lang=en")
    # open Browser in maximized mode
    options.add_argument("start-maximized")
    # disable infobars
    options.add_argument("disable-infobars")
    # disable extension
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

    return driver

def scrape(username, password, driver):
    driver = driver
    driver.get("https://business.facebook.com/")
    time.sleep(10)

    driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div/div/div/div[6]/div/button').click() # Find and click login with Instagram button
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(username) # Find and enter username
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password) # Find and enter password
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]').click() # Find and click login button
    time.sleep(10)
    driver.get("https://business.facebook.com/")
    time.sleep(10)
    driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div/div/div/div[6]/div/button').click() # Find and click login with Instagram button
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div[1]/nav/ul/div/div[7]/div/div/div/li/div/div/a').click()
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[4]/div[1]/div[1]/div/div/div/div/div[3]/div/div/div').click() # Find and click login with Instagram button
    time.sleep(10)

    # return print(profile_data)

scrape("abacoconsultoriajr", "Abacomaiorem5anos", driversetup())
