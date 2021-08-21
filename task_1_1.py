import requests
from pprint import pprint

user_name = 'VadPA'

url = 'https://api.github.com/users/' + user_name + '/repos'
my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/92.0.4515.159 Safari/537.36',
              'Accept': '*/*'}

my_params = {'per_page': 10}

response = requests.get(url, params=my_params, headers=my_headers)
j_data = response.json()

# pprint(j_data)

for i in range(len(j_data)):
    print(j_data[i].get('name'))

print()
