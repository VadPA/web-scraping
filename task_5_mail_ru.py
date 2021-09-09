import time
from datetime import date
from datetime import datetime
from pprint import pprint
from datetime import timedelta

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pymongo import MongoClient

# -------------------------------------------------------------------------------------------------
# Подключаем БД
client = MongoClient('127.0.0.1', 27017)
db = client['letters_email']

letters = db.letters
# -------------------------------------------------------------------------------------------------


dict_month = {'января': "January",
              'февраля': "February",
              'марта': "March",
              'апреля': "April",
              'мая': "May",
              'июня': "June",
              'июля': "July",
              'августа': "August",
              'сентября': "September",
              'октября': "October",
              'ноября': "November",
              'декабря': "December"}

dict_month_num = {'January': "01",
                  'February': "02",
                  'March': "03",
                  'April': "04",
                  'May': "05",
                  'June': "06",
                  'July': "07",
                  'August': "08",
                  'September': "09",
                  'October': "10",
                  'November': "11",
                  'December': "12"}

chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get("https://mail.ru")

log = 'study.ai_172'
login = driver.find_element('name', 'login')
login.send_keys(log)

button = driver.find_element_by_xpath("//button[contains(@class,'button svelte')]")
button.click()

time.sleep(3)

passw = driver.find_element_by_xpath("//div[contains(@class,'password')]/input")
passw.send_keys('NextPassword172???')

button_second = driver.find_element_by_xpath("//button[contains(@class,'second-button')]")
button_second.click()

time.sleep(3)

list_letters = []

def read_date_time(date_):
    part_date = date_.split(', ')[0]
    part_time = date_.split(', ')[-1]
    if part_date == 'Сегодня':
        temp_date = date.today()  # datetime.now().day
        part_date = temp_date.strftime('%d-%m-%Y')
    elif part_date == 'Вчера':
        temp_date = datetime.now() - timedelta(days=1)  # datetime.now().day
        part_date = temp_date.strftime('%d-%m-%Y')
    else:
        date_month = dict_month[part_date.split(" ")[-1]]
        date_day = part_date.split(" ")[0]
        if len(date_day) == 1:
            date_day = '0' + date_day
        part_date = date_day + '-' + dict_month_num[date_month]
        if len(part_date.split(' ')) < 3:
            part_date = part_date + '-' + str(datetime.now().year)
    return part_date, part_time


for j in range(2):
    actions = ActionChains(driver)
    list_letter = driver.find_elements_by_xpath("//div[contains(@class,'dataset__items')]/a")

    for i, el in enumerate(list_letter):
        dict_letter = {}
        flag_letter = driver.find_element_by_xpath("//a[" + str(i + 1) + "]//div[contains(@class,'llc__item "
                                                                         "llc__item_flag')]/button").get_attribute(
            'title')
        if flag_letter == 'Пометить флажком':
            flag = False
        else:
            flag = True
        if not flag:
            heading_letter = driver.find_element_by_xpath("//a[" + str(
                i + 1) + "]//div[contains(@class,'llc__container')]//div[contains(@class,'llc__item "
                         "llc__item_title')]//span[contains(@class,'llc__subject')]")
            info_letter = driver.find_element_by_xpath("//a[" + str(
                i + 1) + "]//div[contains(@class,'llc__container')]//div[contains(@class,'llc__item "
                         "llc__item_title')]//span[contains(@class,'ll-sp__normal')]")
            element_span = driver.find_element_by_xpath(
                "//a[" + str(i + 1) + "]//div[contains(@class,'llc__item llc__item_correspondent')]/span[@title]")
            element_title = str(element_span.get_attribute('title'))
            date_time = read_date_time(driver.find_element_by_xpath(
                "//a[" + str(i + 1) + "]//div[@class='llc__item llc__item_date']").get_attribute('title'))

            dict_letter['link'] = el.get_attribute('href')
            dict_letter['heading_letter'] = heading_letter.text
            dict_letter['info_letter'] = info_letter.text
            dict_letter['email_author'] = element_title.split(' ')[-1].lstrip('<').rstrip('>')
            dict_letter['author'] = element_title.replace(element_title.split(' ')[-1], '').rstrip()
            # dict_letter['date'] = datetime.strptime(date_time[0], '%d-%m-%Y')
            dict_letter['date_time'] = datetime.strptime(date_time[0] + ' ' + date_time[1], '%d-%m-%Y %H:%M')

            list_letters.append(dict_letter)

            button_flag = driver.find_element_by_xpath("//a[" + str(i + 1) + "]//div[contains(@class,'llc__item "
                                                                             "llc__item_flag')]/button["
                                                                             "@title='Пометить флажком']")
            button_flag.click()
            time.sleep(1)

    # actions.move_to_element(list_letter[-1]).perform()
    # list_letter = []
    time.sleep(3)

pprint(list_letters)

for el in list_letters:
    letters.insert_one({
        "link": el['link'],
        "heading_letter": el['heading_letter'],
        "info_letter": el['info_letter'],
        "email_author": el['email_author'],
        "author": el['author'],
        "date_time": el['date_time'],
    })

print()

