import os
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

XPATHS = {
    'login_email': '//*[@id="input_0"]',
    'login_password': '//*[@id="input_1"]',
    'login_button': '/html/body/login-dialog/div/login/div/form/div[4]/div[1]/div[3]/div/button',
    'analytics_page': '//*[@id="root"]/div[2]/div/div/span/section/div/nav/ul/div[9]/div/div/a/li/span',
    'traffic_analytics_page': '//*[@id="root"]/div[2]/div/div/span/section/div/nav/ul/div[9]/ul/a[1]/li/span/div',
    'sessions': '//*[@id="root"]/div[2]/div/div/div/div[2]/main/span/div/div/div[1]/div/div/span/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/h4',
    'visitors': '//*[@id="root"]/div[2]/div/div/div/div[2]/main/span/div/div/div[1]/div/div/span/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[3]/div/div[2]/div/div/div/h4',
    'time_on_site': '//*[@id="root"]/div[2]/div/div/div/div[2]/main/span/div/div/div[1]/div/div/span/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[5]/div/div[2]/div/div/div/h4',
    'behavior_analytics_page': '//*[@id="root"]/div[2]/div/div/span/section/div/nav/ul/div[9]/ul/a[4]/li/span/div',
    'rejection_rate': '//*[@id="root"]/div[2]/div/div/div/div[2]/main/span/div/div/div[1]/div/div/span/div/div/div/div/div[2]/div/div[3]/div[1]/div/div[1]/div/div/div[3]/div/div[2]/div/div/div/h4',
    'mean_pages_per_section': '//*[@id="root"]/div[2]/div/div/div/div[2]/main/span/div/div/div[1]/div/div/span/div/div/div/div/div[2]/div/div[3]/div[1]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/h4'
}

class Scraper:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')
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
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        return driver
    
    def _wait_for_element(self, xpath, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def _login(self):
        try:
            self.driver.get('https://users.wix.com/signin?overrideLocale=pt')
            email_field = self._wait_for_element(XPATHS['login_email'])
            email_field.click()
            email_field.send_keys(self.email)
            self._wait_for_element(XPATHS['login_button']).click()
            password_field = self._wait_for_element(XPATHS['login_password'])
            password_field.click()
            password_field.send_keys(self.password)
            self._wait_for_element(XPATHS['login_button']).click()
        except Exception as e:
            print(f"Error during login: {e}")

    def _fetch_traffic_data(self):
        try:
            analytics_page = self._wait_for_element(XPATHS['analytics_page'])
            analytics_page.click()
            traffic_analytics_page = self._wait_for_element(XPATHS['traffic_analytics_page'])
            traffic_analytics_page.click()
            sessions = self._wait_for_element(XPATHS['sessions']).text
            visitors = self._wait_for_element(XPATHS['visitors']).text
            time_on_site = self._wait_for_element(XPATHS['time_on_site']).text
            return {
                'sessions': sessions,
                'visitors': visitors,
                'time': time_on_site
            }
        except Exception as e:
            print(f"Error fetching traffic data: {e}")
            return {}

    def _fetch_behavior_data(self):
        try:
            behavior_analytics_page = self._wait_for_element(XPATHS['behavior_analytics_page'])
            behavior_analytics_page.click()
            rejection_rate = self._wait_for_element(XPATHS['rejection_rate']).text
            mean_pages_per_section = self._wait_for_element(XPATHS['mean_pages_per_section']).text
            return {
                'rejection_rate': rejection_rate,
                'mean_pages_per_section': mean_pages_per_section
            }
        except Exception as e:
            print(f"Error fetching behavior data: {e}")
            return {}

    def scrape_data(self):
        self._login()
        traffic_data = self._fetch_traffic_data()
        behavior_data = self._fetch_behavior_data()
        self.driver.quit()
        return {**traffic_data, **behavior_data}

class DataSaver:
    @staticmethod
    def save(data):
        df = pd.DataFrame(data, index=[0])
        if not os.path.isfile('blog_data.csv'):
            df.to_csv('blog_data.csv', index=False)
        else:
            existing_df = pd.read_csv('blog_data.csv')
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_csv('blog_data.csv', index=False)

if __name__ == "__main__":
    scraper = Scraper()
    data = scraper.scrape_data()
    DataSaver.save(data)
