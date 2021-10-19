import pymysql
import requests
import json
import pandas as pd
date_year = 2021
date_month = 10
date_day = 12
requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接


# 从db中获取block信息
def getBlockInfo(num):
    block_info = []
    # 连接数据库
    db = pymysql.connect(host='rm-2zetcrfz7vg3ay7do125030pm.mysql.rds.aliyuncs.com',
                         user='r_fb_buddels_users',
                         password='EqgJoRLguk2CKrMZ',
                         db='fb_buddles')
    cur = db.cursor()
    # 筛选block
    sql = f"select block_number,transaction_num,gas_price from block_info where finish_time between \'{date_year}-{date_month}-{date_day} 00:00:00\' and \'{date_year}-{date_month}-{date_day + 1} 00:00:00\' limit " + str(num)
    print(sql)
    row_count = cur.execute(sql)
    print("length: ", row_count)
    # 将tuple转换为list存入block_info
    for bi in cur.fetchall():
        block_info.append(list(bi))
    print(block_info)
    db.close()
    return block_info


# 从 flashbot api 获取fb交易信息
def getFlashBot(block_num):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    headers = {'User-Agent': user_agent}
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    url = 'https://blocks.flashbots.net/v1/blocks?block_number=' + str(block_num)
    r = requests.get(url, headers=headers, proxies=proxies)
    return json.loads(r.text)


def getFbFromDb(block_num):
    fb_info = []
    # 连接数据库
    db = pymysql.connect(host='rm-2zetcrfz7vg3ay7do125030pm.mysql.rds.aliyuncs.com',
                         user='r_fb_buddels_users',
                         password='EqgJoRLguk2CKrMZ',
                         db='fb_buddles')
    cur = db.cursor()
    # 筛选block
    sql = f"select * from transaction_info where block_num_id = {block_num}"
    print("fb sql: ", sql)
    row_count = cur.execute(sql)
    print("fb length: ", row_count)
    # 将tuple转换为list存入block_info
    for fb in cur.fetchall():
        fb_info.append(list(fb))
    db.close()
    # 把list转为df
    # print(fb_info)
    fb_df = pd.DataFrame(fb_info,
                         columns=('transaction_hash', 'bundle_index', 'tx_index', 'eoa_address', 'to_address',
                                  'gas_used', 'gas_price', 'coinbase_transfer', 'miner_reward', 'block_num_id',
                                  'finish_time', 'timestamp'))
    # print(fb_df)
    return fb_df


if __name__ == '__main__':
    block_info = getBlockInfo(1000)
    # print(getFlashBot(13398252))
    # fb_data = getFbFromDb(13398252)
    # buddle_index = 0
    # sum_gasFee = 0
    # sum_gasUsed = 0
    # buddle_gasPrice = []
    # for i in range(len(fb_data)):
    #     fbi = fb_data.iloc[i]
    #     if fbi['bundle_index'] == buddle_index:
    #         sum_gasFee += int(fbi['gas_price']) * int(fbi['gas_used'])
    #         sum_gasUsed += int(fbi['gas_used'])
    #     else:
    #         buddle_gasPrice.append(sum_gasFee/sum_gasUsed)
    #         buddle_index += 1
    #         sum_gasFee = 0
    #         sum_gasUsed = 0
    #         sum_gasFee += int(fbi['gas_price']) * int(fbi['gas_used'])
    #         sum_gasUsed += int(fbi['gas_used'])
    # buddle_gasPrice.append(sum_gasFee/sum_gasUsed)
    # print(f"buddle_index: {buddle_index}")
    # print(f"buddle_gasPrice: {buddle_gasPrice}")
    # fb_min = min(buddle_gasPrice)
    # print(f"fb_min: {fb_min}")




