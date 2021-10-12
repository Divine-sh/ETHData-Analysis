import pymysql
from web3 import Web3
provider = "ws://172.17.31.104:3334"
w3 = Web3(Web3.WebsocketProvider(provider))
connectStatus = w3.isConnected()
print(f"web3 is connected:{connectStatus}")


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
    sql = "select block_number,transaction_num,gas_price from block_info where finish_time between '2021-10-12 00:00:00' and '2021-10-13 00:00:00' limit " + str(num)
    row_count = cur.execute(sql)
    print("length: ", row_count)
    # 将tuple转换为list存入block_info
    for bi in cur.fetchall():
        block_info.append(list(bi))
    print(block_info)
    db.close()
    return block_info



if __name__ == '__main__':
    getBlockInfo(50)




