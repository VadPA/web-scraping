import json
import time
from pprint import pprint

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

# -------------------------------------------------------------------------------------------------
# Подключаем БД
client = MongoClient('127.0.0.1', 27017)
db = client['new_items_mvideo']

items = db.new_items
# -------------------------------------------------------------------------------------------------


chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get("https://mvideo.ru")

driver.implicitly_wait(10)

actions = ActionChains(driver)
actions.move_by_offset(100, 100).click()
actions.perform()

time.sleep(3)
notExit = True
li = []

actions = ActionChains(driver)
articles = driver.find_elements_by_xpath("//div[contains(@class,'facelift gallery-layout')]")
actions.move_to_element(articles[-3]).perform()
time.sleep(5)

button_right_scroll = driver.find_element_by_xpath("//div[contains(@class,'facelift gallery-layout')][2]//a[contains(@class,'right')]")
list_tag_new_products = []
list_products = []

while notExit:
    while button_right_scroll.get_attribute('class') != 'next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right disabled':
        button_right_scroll.click()
        time.sleep(2)
    li = driver.find_elements_by_xpath("//div[contains(@class,'facelift gallery-layout')][2]//h3")
    list_tag_new_products = driver.find_elements_by_xpath("//div[contains(@class,'facelift gallery-layout')][2]//h3//a")
    notExit = False

for el in list_tag_new_products:
    dict_prod = json.loads(el.get_attribute('data-product-info').replace("'", '"'))
    dict_prod['productPriceLocal'] = float(dict_prod['productPriceLocal'])

    list_products.append(dict_prod)
    pprint(dict_prod)

for el in list_products:
    items.insert_one({
        "Location": el['Location'],
        "eventPosition": el['eventPosition'],
        "productCategoryId": el['productCategoryId'],
        "productCategoryName": el['productCategoryName'],
        "productGroupId": el['productGroupId'],
        "productId": el['productId'],
        "productName": el['productName'],
        "productPriceLocal": el['productPriceLocal'],
        "productVendorName": el['productVendorName'],
    })

