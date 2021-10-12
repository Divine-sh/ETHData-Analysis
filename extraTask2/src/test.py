import requests
import json
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
headers = {'User-Agent': user_agent}
r = requests.get('https://blocks.flashbots.net/v1/blocks?block_number=12073997')
# print(type(r.text))
# print(r.text)
print(type(json.loads(r.text)))
print(json.loads(r.text))
