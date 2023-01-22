import time
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

s = Service('./chromedriver.exe')

chromeOptions = Options()
chromeOptions.add_argument('start-maximized')

driver = webdriver.Chrome(service=s, options=chromeOptions)
driver.implicitly_wait(10)
driver.get('https://mvideo.ru/')

time.sleep(5)
driver.find_elements(By.TAG_NAME, 'body')[0].send_keys(Keys.END)
time.sleep(5)

try:
    btn_trend = driver.find_elements(By.XPATH, "//button[@class='tab-button ng-star-inserted']")[0]
    btn_trend.click()
except NoSuchElementException:
    print('Кнопка не найдена')

while True:
    wait = WebDriverWait(driver, 15)
    try:
        button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                        "//button[@class='btn mv-icon-button--primary  mv-icon-button--medium mv-button mv-icon-button']")))
        button.click()
    except TimeoutException:
        print("Скролл окончен")
        break

goods = driver.find_elements(By.XPATH, "//div[@class='product-mini-card__name ng-star-inserted']/div/a")

client = MongoClient('localhost', 27017)
mongobase = client.vacancies_cppdev_hh
collection = mongobase["Mvid"]

for gd in goods:
    good_url = gd.get_attribute('href')
    good_name = gd.find_element(By.XPATH, ".//div").text
    collection.insert_one({'name': good_name, 'url': good_url})



