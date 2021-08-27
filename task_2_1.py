from pprint import pprint

from bs4 import BeautifulSoup as bs
import requests


# '': '',
# '': '',
# '': '',
# '': '',
# '': '',
# '': '',
# '': '',
# '': '',
# '': '',

def read_page(div_list):
    list_vak_temp = []
    for el in div_list:
        try:
            element = el.find('a')
            # l = element['href']
            link_vak = el.find('a').attrs.get('href')
            if url2 in link_vak:
                vak_data = {}
                vakansia = el.find('a').text
                link_vakansia = url1 + link_vak
                tag_vak_salary = el.find('span', attrs={'class': 'f-test-text-company-item-salary'})
                vak_salary = tag_vak_salary.text.replace('\xa0', ' ')

                vak_data['vakansia'] = vakansia
                vak_data['vak_salary'] = vak_salary
                vak_data['link_vakansia'] = link_vakansia
                list_vak_temp.append(vak_data)
        except:
            continue
    return list_vak_temp


url1 = 'https://www.superjob.ru'
url2 = '/vakansii/'
pages = 0
vac = ''
vakansii = ''
list_vak = []

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/92.0.4515.159 Safari/537.36'}

list_vac = {'IT, Интернет, связь, телеком': 'it-internet-svyaz-telekom',
            'Административная работа, секретариат, АХО': 'administrativnaya-rabota-sekretariat-aho',
            'Банки, инвестиции, лизинг': 'banki-investicii-lizing',
            'Безопасность, службы охраны': 'bezopasnost-sluzhby-ohrany',
            'Бухгалтерия, финансы, аудит': 'buhgalteriya-finansy-audit',
            'Государственная служба': 'gosudarstvennaya-sluzhba',
            'Дизайн': 'dizajn',
            'Домашний персонал': 'domashnij-personal',
            'Закупки, снабжение': 'zakupki-snabzhenie',
            'Искусство, культура, развлечения': 'iskusstvo-kultura-razvlecheniya',
            'Кадры, управление персоналом': 'kadry-upravlenie-personalom',
            'Консалтинг, стратегическое развитие': 'konsalting-strategicheskoe-razvitie',
            'Маркетинг, реклама, PR': 'marketing-reklama-pr'}

print('Отрасли, по которым есть вакансии:')

for i, el in enumerate(list_vac):
    print(f' {i}. {el}')

print('Выберите вакансию по отрасли:')

num_vac = int(input())

for i, el in enumerate(list_vac):
    if i == num_vac:
        vakansii = el
        vac = list_vac.get(el)
        break

link = url1 + url2 + vac + '/'

response = requests.get(link, headers=headers)

soup = bs(response.text, 'html.parser')

list_href = soup.find('a', attrs={'class': 'f-test-link-Dalshe'})

if list_href:
    pages = int(list_href.previous_sibling.text)

div_list = soup.find_all('div', attrs={'class': 'f-test-search-result-item'})

list_vak = read_page(div_list)

for i in range(2, pages + 1):
    link_page = link + '?page=' + str(i)
    response = requests.get(link_page, headers=headers)
    soup = bs(response.text, 'html.parser')
    div_list = soup.find_all('div', attrs={'class': 'f-test-search-result-item'})
    list_vak.extend(read_page(div_list))

pprint(list_vak)
print(f'Всего вакансий в категории "{vakansii}" - {len(list_vak)}')

# pprint()
