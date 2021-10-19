import pandas as pd
import requests
import json
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
headers = {'User-Agent': user_agent}
# r = requests.get('https://blocks.flashbots.net/v1/blocks?block_number=12073997')
# print(type(r.text))
# print(r.text)
# print(type(json.loads(r.text)))
# print(json.loads(r.text))
# df_out = pd.DataFrame(columns=['block_num', 'fb_min', 'nfb_max', 'exist_high_priority', 'high_priority_account'])
# df_out.loc[0] = [1213213, 23232, 343434, 0, ['a','b','v']]
# df_out.to_csv('default.csv')
# 构造一个空的dataframe

df = pd.DataFrame(columns=['name', 'number'])
print(df)
# 采用.loc的方法进行
df.loc[0] = ['cat', 3]  # 其中loc[]中需要加入的是插入地方dataframe的索引，默认是整数型
# 也可采用诸如df.loc['a'] = ['123',30]的形式
df.loc['a'] = ['123', 30]
print(df)
print(1e9)

list = [1, 5, 4, 2, 3, 6]
print(list.index(5))
list.sort(reverse=True)
print(list)
print(list.index(5))

