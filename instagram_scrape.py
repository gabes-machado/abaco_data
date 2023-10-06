import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

XPATHS = {
    # Instagram Login XPaths
    'login_with_instagram': '/html/body/div/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div/div/div/div[6]/div/button',
    'username_input': '//*[@id="loginForm"]/div/div[1]/div/label/input',
    'password_input': '//*[@id="loginForm"]/div/div[2]/div/label/input',
    'login_button': '//*[@id="loginForm"]/div/div[3]',
        
    # Instagram Overview Data XPaths
    'insights_page': '/html/body/div[1]/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div[1]/nav/ul/div/div[7]/div/div/li/div/div/a',
    'close_popup': '//*[@id="facebook"]/body/div[4]/div[1]/div[1]/div/div/div/div/div[3]/div/div/div',
    'reach': '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div[2]/div[1]',
    'followers': '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[3]/div/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div[2]/div',
    
    # Instagram Results Data XPaths
    'results_page': '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/div/nav[1]/div[2]/div[2]/div[1]/a/div/div',
    'profile_visits': '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/span[1]',
    'new_followers': '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div[4]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/span[1]',
    
    # Instagram Content Data XPaths
    'content_page': '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/div/nav[2]/div[2]/div[1]/div[1]/a/div/div',
    'post_engagement': '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/div/div[6]/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]',
    
    # Instagram Stories Data XPaths
    'stories_page': '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[4]/div/div/span[1]',
    'story_reach': '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]',
    'story_engagement': '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/div/div[6]/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]',
    'published_stories': '//*[@id="facebook"]/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/div/div[4]/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]'
}

class InstaScraper:
    def __init__(self):
        self.email = 'abacoconsultoriajr'
        self.password = 'Abacomaiorem5anos'
        self.driver = self._setup_driver()
    
    def _setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('lang=en')
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--incognito')
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        return driver
    
    def _wait_for_element(self, xpath, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def _login(self):
        try:
            self.driver.get('https://business.facebook.com/')  # Your initial login URL here
            self._wait_for_element(XPATHS['login_with_instagram']).click()
            self._wait_for_element(XPATHS['username_input']).send_keys(self.email)
            self._wait_for_element(XPATHS['password_input']).send_keys(self.password)
            self._wait_for_element(XPATHS['login_button']).click()
            time.sleep(10)
            self.driver.get('https://business.facebook.com/')
            self._wait_for_element(XPATHS['login_with_instagram']).click()
        except Exception as e:
            print(f"Error during login: {e}")

    def scrape_overview_data(self):
        try:
            time.sleep(5)
            self._wait_for_element(XPATHS['insights_page']).click()
            time.sleep(5)
            self._wait_for_element(XPATHS['close_popup']).click()
            time.sleep(5)
            reach = self._wait_for_element(XPATHS['reach']).text
            followers = self._wait_for_element(XPATHS['followers']).text

            return {
                'username': self.email,
                'reach': reach,
                'followers': followers
            }
        except Exception as e:
            print(f"Error fetching overview data: {e}")
            return {}

    def scrape_results_data(self):
        try:
            time.sleep(5)
            self._wait_for_element(XPATHS['results_page']).click()
            time.sleep(5)
            profile_visits = self._wait_for_element(XPATHS['profile_visits']).text
            new_followers = self._wait_for_element(XPATHS['new_followers']).text

            return {
                'profile_visits': profile_visits,
                'new_followers': new_followers
            }
        except Exception as e:
            print(f"Error fetching results data: {e}")
            return {}

    def scrape_content_data(self):
        try:
            time.sleep(5)
            self._wait_for_element(XPATHS['content_page']).click()
            time.sleep(5)
            post_engagement = self._wait_for_element(XPATHS['post_engagement']).text

            return {
                'post_engagement': post_engagement
            }
        except Exception as e:
            print(f"Error fetching content data: {e}")
            return {}

    def scrape_stories_data(self):
        try:
            time.sleep(5)
            self._wait_for_element(XPATHS['stories_page']).click()
            time.sleep(5)
            story_reach = self._wait_for_element(XPATHS['story_reach']).text
            story_engagement = self._wait_for_element(XPATHS['story_engagement']).text
            published_stories = self._wait_for_element(XPATHS['published_stories']).text

            return {
                'story_reach': story_reach,
                'story_engagement': story_engagement,
                'published_stories': published_stories
            }
        except Exception as e:
            print(f"Error fetching stories data: {e}")
            return {}

    def scrape_data(self):
        self._login()
        overview_data = self.scrape_overview_data()
        results_data = self.scrape_results_data()
        content_data = self.scrape_content_data()
        stories_data = self.scrape_stories_data()
        self.driver.quit()
        return {**overview_data, **results_data, **content_data, **stories_data}

class DataSaver:
    @staticmethod
    def save(data):
        df = pd.DataFrame(data, index=[0])
        df.to_csv('insta_data.csv', index=False)        

        '''
        if not os.path.isfile('insta_data.csv'):
            df.to_csv('insta_data.csv', index=False)
        else:
            existing_df = pd.read_csv('insta_data.csv')
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_csv('insta_data.csv', index=False)
        '''

scraper = InstaScraper()
data = scraper.scrape_data()
DataSaver.save(data)
