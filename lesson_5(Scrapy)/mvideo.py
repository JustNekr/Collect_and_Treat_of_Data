import re
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions as se

client = MongoClient('localhost', 27017)
db = client["mvideo"]

service = Service('./chromedriver.exe')
chrome_options = Options()
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("start-maximized")
# chrome_options.add_argument("--headless")  #с этим вообще не хочет работать

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
driver.get('https://www.mvideo.ru/')

actions = ActionChains(driver)
actions.move_by_offset(100, 100).click().perform()
driver.execute_script("window.scrollTo(0, 1440);")


wait = WebDriverWait(driver, 10)
button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='tab-button ng-star-inserted']")))
button.click()


button = wait.until(EC.presence_of_element_located((By.XPATH, "//mvid-shelf-group/mvid-carousel/div/button[contains(@class, 'forward')]")))
while True:
    try:
        button.click()
    except se.ElementNotInteractableException:    # ElementClickInterceptedException
        break
    except se.ElementClickInterceptedException:
        break


names = driver.find_elements(By.XPATH, "//mvid-shelf-group/mvid-carousel/div/div/mvid-product-cards-group/div["
                                       "contains(@class, 'name')]")
prices = driver.find_elements(By.XPATH, "//mvid-shelf-group/mvid-carousel/div/div/mvid-product-cards-group/div["
                                        "contains(@class, 'price')]")

for name, price in zip(names, prices):
    price = float(re.match(r'\d+', price.text.replace(' ', ''))[0])
    name = name.text
    product = {
        'name': name,
        'price': price
    }

    db.trend_products.update_one({'name': name}, {'$set': product}, upsert=True)

