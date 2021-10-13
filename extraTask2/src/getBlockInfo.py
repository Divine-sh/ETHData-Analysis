import pymysql
import requests
import json

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
    sql = "select block_number,transaction_num from block_info where finish_time between '2021-10-12 00:00:00' and '2021-10-13 00:00:00' limit " + str(num)
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


if __name__ == '__main__':
    getBlockInfo(1000)
    print(getFlashBot(13398252))




