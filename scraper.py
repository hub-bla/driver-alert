from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options



class Scraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new") # for Chrome >= 109
        self.base_url = 'https://tablica-rejestracyjna.pl/'
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    

    def find_license(self, license_text):
        url = "".join([self.base_url, license_text])
        print(url)
        self.browser.get(url)
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR , f"[aria-label=\"Zgadzam się\"]"))
            )
        except:
            return {}
        bttn = self.browser.find_element(By.CSS_SELECTOR, f"[aria-label=\"Zgadzam się\"]")
        bttn.click()

        comments_obs = self.browser.find_elements(By.CLASS_NAME, "comment")
        comments = {}
        for comment in comments_obs:
            text = comment.find_element(By.CLASS_NAME, "text").text
            date = comment.find_element(By.CLASS_NAME, "date").text
            comments[date] = text
        rate_btn = self.browser.find_elements(By.CLASS_NAME, "fingerUp")
        if rate_btn is None:
            return {}
        print("COMMENTS", comments)
        print("URL: ", url) 
        return comments
    

 
