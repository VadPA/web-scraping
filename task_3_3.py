from pymongo import MongoClient
from typing import List, Dict, Any
from pprint import pprint
from bs4 import BeautifulSoup as bs

import requests

# -------------------------------------------------------------------------------------------------
url1 = 'https://hh.ru'
url2 = '/vacancies/'

my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/92.0.4515.159 Safari/537.36',
              'Accept': '*/*'}

rus_char = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z',
            'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
            'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
            'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '_'}
# -------------------------------------------------------------------------------------------------
# Подключаем БД
client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']

vacancy = db.vacancy


# -------------------------------------------------------------------------------------------------

def translate(word):
    return "".join([rus_char[el] for el in list(word)])


def cleaning_str_num(s):
    return "".join([el for el in list(s) if 48 <= ord(el) <= 57])


def cleaning_str_char(s):
    return "".join([el for el in list(s) if ord(el) > 57])


def analysis_str(line):
    dict_salary = {'min': '', 'max': '', 'currency': ''}
    if chr(8211) in line:
        if (('от' in line) & ('до' in line)) \
                | (('от' not in line) & ('до' not in line)):
            min_str, ch, max_str = line.partition(chr(8211))
            dict_salary['min'] = int(cleaning_str_num(min_str))
            dict_salary['max'] = int(cleaning_str_num(max_str))
            dict_salary['currency'] = cleaning_str_char(max_str)
        # elif 'от' in line:
        #     min_str, ch, max_str = line.rpartition('от')
        #     dict_salary['min'] = cleaning_str_num(line)
        #     dict_salary['currency'] = cleaning_str_char(max_str)
        # elif 'до' in line:
        #     min_str, ch, max_str = line.rpartition('до')
        #     dict_salary['max'] = cleaning_str_num(line)
        #     dict_salary['currency'] = cleaning_str_char(max_str)
    elif 'от' in line:
        min_str, ch, max_str = line.rpartition('от')
        dict_salary['max'] = None
        dict_salary['min'] = int(cleaning_str_num(line))
        dict_salary['currency'] = cleaning_str_char(max_str)
    elif 'до' in line:
        min_str, ch, max_str = line.rpartition('до')
        dict_salary['min'] = None
        dict_salary['max'] = int(cleaning_str_num(line))
        dict_salary['currency'] = cleaning_str_char(max_str)
    return dict_salary


def read_list_tag_vac(div_list):
    list_vac_temp: List[Dict[str, Any]] = []
    for el in div_list:
        try:
            vac_data = {}
            vacancy = el.find('a', attrs={'class': 'bloko-link'}).text
            link_vac = el.find('a').attrs.get('href')
            try:
                tag_vac_salary = el.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            except:
                tag_vac_salary = None
            tag_vac_employer = el.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            tag_link_employer = url1 + el.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).attrs.get(
                'href')

            vac_data['vacancy'] = vacancy
            vac_data['link_vac'] = link_vac
            vac_data['vac_employer'] = tag_vac_employer.replace('\xa0', ' ')
            vac_data['link_employer'] = tag_link_employer

            if tag_vac_salary:
                salary = analysis_str(tag_vac_salary.replace('\u202f', ' '))
                vac_data['vac_salary_min'] = salary['min']
                vac_data['vac_salary_max'] = salary['max']
                vac_data['vac_salary_currency'] = salary['currency']
                vac_data['vac_salary'] = tag_vac_salary.replace('\u202f', ' ')
            else:
                vac_data['vac_salary_min'] = None
                vac_data['vac_salary_max'] = None
                vac_data['vac_salary_currency'] = None
                vac_data['vac_salary'] = None

            list_vac_temp.append(vac_data)
        except:
            continue
    return list_vac_temp


s = input('Введите специальность: ')

speciality = translate(s)
response = requests.get(url1 + url2 + speciality, headers=my_headers)
soup = bs(response.text, 'html.parser')
tag_block_vac = soup.find('div', attrs={'class': 'bloko-gap bloko-gap_s-top bloko-gap_m-top bloko-gap_l-top'})
tag_parent = tag_block_vac.parent

tag_pager_scroll = tag_parent.find('div', attrs={'class': 'bloko-gap bloko-gap_top'})

if tag_pager_scroll:
    tag_pager_block = tag_pager_scroll.find('div', attrs={'data-qa': 'pager-block'})
    tag_end = tag_pager_block.find('span', attrs={'class': 'bloko-form-spacer'})
    pages = int(tag_end.previous_element)
else:
    pages = 1

list_vac = []
list_tag_vac = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
list_vac.extend(list_tag_vac)

for i in range(1, pages):
    link_page = url1 + url2 + speciality + '?page=' + str(i)
    response = requests.get(link_page, headers=my_headers)
    soup = bs(response.text, 'html.parser')
    list_tag_vac = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    list_vac.extend(list_tag_vac)

result_list = read_list_tag_vac(list_vac)


def check_for_entry(item):
    bool_ = False
    for element in vacancy.find({}):
        if (element['employer'] == item['vac_employer']) & (element['vacancy'] == item['vacancy']) \
                & (
                (element['salary_min'] == item['vac_salary_min']) | (element['salary_max'] == item['vac_salary_max'])):
            bool_ = True
            break
        else:
            continue
    return bool_


for el in result_list:
    new_vac = False
    if not check_for_entry(el):
        vacancy.insert_one({
            "employer": el['vac_employer'],
            "link_employer": el['link_employer'],
            "vacancy": el['vacancy'],
            "link_vacancy": el['link_vac'],
            "salary_min": el['vac_salary_min'],
            "salary_max": el['vac_salary_max'],
            "salary_currency": el['vac_salary_currency'],
        })
        new_vac = True
        print('Ура новая вакансия:')
        pprint(el)

if not new_vac:
    print('Новых вакансий нет.')

print()
