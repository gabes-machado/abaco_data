from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def driversetup():
    options = webdriver.ChromeOptions()
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
    
    time.sleep(5)
    
    driver.get("https://business.facebook.com/") # Going to the url
    time.sleep(5)

    driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div/div/div/div[6]/div/button').click() # Find and click login with Instagram button
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(username) # Find and enter username
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password) # Find and enter password
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]').click() # Find and click login button
    time.sleep(5)
    driver.get("https://business.facebook.com/") # Work around the login bug
    time.sleep(5)
    driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div/div/div/div[6]/div/button').click() # Find and click login with Instagram button
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div[1]/nav/ul/div/div[7]/div/div/div/li/div/div/a').click() # Getting in the insights page
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[4]/div[1]/div[1]/div/div/div/div/div[3]/div/div/div').click() # Closing pup-up window
    time.sleep(5)
   
    overview_data = {
        'username': username,
        'reach': driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div[2]/div[1]').text,
        'followers': driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[3]/div/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div[2]/div').text
        }
    
    driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/div/nav[1]/div[2]/div[2]/div[1]/a/div/div').click()
    time.sleep(5)

    results_data = {
        'profile_visits': driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/span[1]').text,
        'new_followers': driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div[4]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/span[1]').text
    }

    driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/div/nav[2]/div[2]/div[1]/div[1]/a/div/div').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[3]/div/div/span[1]').click()
    time.sleep(5)

    content_data = {
        'post_engagement': driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/div/div[6]/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]').text
    }

    driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[4]/div/div/span[1]').click()
    time.sleep(5)

    stories_data = {
        'story_reach': driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]').text,
        'story_engagement': driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/div/div[6]/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]').text,
        'published_stories': driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/div/div[4]/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]').text
    }

    data = overview_data | results_data | content_data | stories_data

    return data

username = str(input("Enter your username: "))
password = str(input("Enter your password: "))

instagram_data = scrape(username, password, driversetup())

df = pd.DataFrame(instagram_data, index=[0])
df.to_csv('instagram_data.csv', index=False)
