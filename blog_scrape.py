from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

def driversetup():
    options = webdriver.ChromeOptions()
    # overcome limited resource problems
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('lang=en')
    # open Browser in maximized mode
    options.add_argument('start-maximized')
    # disable infobars
    options.add_argument('disable-infobars')
    # disable extension
    options.add_argument('--disable-extensions')
    options.add_argument('--incognito')
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

    return driver

def scrape(email, password, driver):
    driver = driver

    time.sleep(5)

    driver.get('https://users.wix.com/signin?overrideLocale=pt') # Going to the url
    time.sleep(5)
    
    driver.find_element(By.XPATH, '//*[@id="input_0"]').click()
    driver.find_element(By.XPATH, '//*[@id="input_0"]').send_keys(email) # Find and enter username
    time.sleep(5)
    
    driver.find_element(By.XPATH, '/html/body/login-dialog/div/login/div/form/div[4]/div[1]/div[3]/div/button').click() # Find and click login button
    time.sleep(5)

    
    driver.find_element(By.XPATH, '//*[@id="input_1"]').click()
    driver.find_element(By.XPATH, '//*[@id="input_1"]').send_keys(password) # Find and enter password
    time.sleep(5)

    
    driver.find_element(By.XPATH, '/html/body/login-dialog/div/login/div/form/div[4]/div[1]/div[3]/div/button').click() # Find and click login button
    time.sleep(5)

    
    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/span/section/div/nav/ul/div[9]/div/div/a/li/span').click() # Getting in the analytics page
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/span/section/div/nav/ul/div[9]/ul/a[1]/li/span/div').click() # Getting in the traffic analytics page
    time.sleep(5)

    traffic_data = {
        'sessions': driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/div/div[2]/main/span/div/div/div[1]/div/div/span/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/h4').text,
        'visitors': driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/div/div[2]/main/span/div/div/div[1]/div/div/span/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[3]/div/div[2]/div/div/div/h4').text,
        'time': driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/div/div[2]/main/span/div/div/div[1]/div/div/span/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[5]/div/div[2]/div/div/div/h4').text
         }
    
    
    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/span/section/div/nav/ul/div[9]/ul/a[4]/li/span/div').click() # Getting in the behavior analytics page
    time.sleep(5)

    behavior_data = {
        'rejection_rate': driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/div/div[2]/main/span/div/div/div[1]/div/div/span/div/div/div/div/div[2]/div/div[3]/div[1]/div/div[1]/div/div/div[3]/div/div[2]/div/div/div/h4').text,
        'mean_pages_per_section': driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/div/div[2]/main/span/div/div/div[1]/div/div/span/div/div/div/div/div[2]/div/div[3]/div[1]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/h4').text
    }

    data = traffic_data | behavior_data

    driver.quit()

    return data


username = str(input("Enter your username: "))
password = str(input("Enter your password: "))

blog_data = scrape(username, password, driversetup())

df = pd.DataFrame(blog_data, index=[0])

if not os.path.isfile('blog_data.csv'):
    df.to_csv('blog_data.csv', index=False)
else:
    existing_df = pd.read_csv('blog_data.csv')
    updated_df = pd.concat([existing_df, df], ignore_index=True)
    updated_df.to_csv('blog_data.csv', index=False)
    