import requests
from pprint import pprint

user_name = 'VadimQuant'
api_key = 'api_key=6369d2e174f84aeea4b9bc3060xxxxxx'
token = '&token=0feaf4eb336825e975bf813d45xxxxxx'
url = 'https://www.last.fm/api/auth/?' + api_key + token
my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/92.0.4515.159 Safari/537.36',
              'Accept': '*/*'}

response = requests.get(url, headers=my_headers)


j_data = response.ok

# pprint(j_data)

print(str(j_data))

# True
#
# Process finished with exit code 0
