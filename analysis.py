import json
import time
import pandas as pd
import numpy as np
from selenium import webdriver
from web3 import Web3

# 不使用科学计数法
# pd.set_option('display.float_format', lambda x: '%.3f' % x)
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# x就是你要设置的显示的宽度，防止轻易换行
pd.set_option('display.width', None)


def info_extract():
    # 读取csv文件
    df = pd.read_csv('research.csv')
    df_gasUsed = pd.read_csv('gasUsed.csv')
    c1 = ("txHash", "blockNumber", "我方time", "我方gasPrice", "我方toMiner", "我方gasUsed", "我方折算")
    c2 = ("是否N+2", "是否抢机会", "对方botTime", "对方gasPrice", "对方toMiner", "对方gasUsed", "对方折算")
    df_out = pd.DataFrame(columns=c1+c2)
    print("The amount of transaction is: ", len(df))
    for i in range(len(df)):
        print("第%s笔交易: " % i)
        # --------------------------------------------------------------------------
        # 获取日志中第i笔交易数据
        inf = df.iloc[i, ]
        # txHash
        # print("txHash:", inf.txHash)
        # block号(日志中)
        # print("blockNumber:", inf.blockNumber)
        start = len("final contract params are ,")
        json_data = json.loads(inf.msg[start:])
        # 我方时间
        timeArray = time.localtime(inf.logTime)
        my_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # print("我方时间:", my_time)
        # 我方gasPrice
        my_gasPrice = int(json_data['overrides']['maxFeePerGas']['hex'], 16)
        # print("我方gasPrice:", my_gasPrice)
        # 我方toMiner
        my_toMiner = int(json_data['_ethAmountToCoinbase']['hex'], 16)
        # print("我方toMiner:", my_toMiner)
        # 我方gasUsed
        # print(inf.txHash)
        df_GU = df_gasUsed[df_gasUsed['txHash'] == inf.txHash]
        if df_GU.empty:
            my_gasUsed = 1
        else:
            my_gasUsed = df_gasUsed[df_gasUsed['txHash'] == inf.txHash].iloc[0, 1]
        # print("我方gasUsed:", my_gasUsed)
        # 我方折算
        my_gasCal = (my_gasPrice * my_gasUsed + my_toMiner) / my_gasUsed
        # print("我方折算:", my_gasCal)
        # --------------------------------------------------------------------------
        # 通过selenium爬取stauts、blockNumber和交易token种类,判断交易类型
        res1 = get_status_and_token(inf.txHash, inf.blockNumber)
        if res1[0] == "yes":
            token1 = res1[1]
            print("token1:", token1)
        else:
            df_out.loc[i] = [inf.txHash, inf.blockNumber, my_time, my_gasPrice, my_toMiner, my_gasUsed, my_gasCal, res1[0], "no", None, None, None, None, None]
            continue

        # 通过web3得到交易的blockNumber和transactionIndex，
        # 调用Eth.get_transaction_by_block( blockNumber , transactionIndex+1 )来获得对手交易txHash
        op_txHash = get_opponent_txHash(inf.txHash)

        # 通过selenium爬取对手的token种类，timestamp，toMiner，gasPrice，gasUsed,判断对手token是否与日志交易tokn有相同
        op_info = get_opponent_info(op_txHash, token1)

        # --------------------------------------------------------------------------
        # 输出到csv
        if op_info[0] != "yes":
            df_out.loc[i] = [inf.txHash, inf.blockNumber, my_time, my_gasPrice, my_toMiner, my_gasUsed, my_gasCal, res1[0], op_info[0], None, None, None, None, None]
        else:
            df_out.loc[i] = [inf.txHash, inf.blockNumber, my_time, my_gasPrice, my_toMiner, my_gasUsed, my_gasCal, res1[0], op_info[0], op_info[1], op_info[2], op_info[3], op_info[4], op_info[5]]
        # df_out.to_csv("output.csv", encoding="utf_8_sig")
        # --------------------------------------------------------------------------
    print(df_out)
    df_out.to_csv("output.csv", encoding="utf_8_sig")
    return df_out


def get_status_and_token(txHash, logBlock):
    # 通过selenium爬取stauts、blockNumber和交易token种类
    # default1：若status不为suscess，在是否为N+2列输出not exist或fail
    # default2：若status为success，分析是否为N+2，否则输出no
    # 返回值: list
    # 首位: 不存在（not exist），失败（fail），不为N+2（no），符合（yes）
    # 符合的话之后为: 交易token种类（list）
    res_name = ["not exist", "fail", "no", "yes"]
    res = []
    url = 'https://etherscan.io/tx/' + txHash
    # 初始化一个浏览器
    driver = webdriver.Chrome()
    driver.get(url)
    # 隐式等待
    driver.implicitly_wait(2)
    # 查找元素
    infs = driver.find_elements_by_class_name('row.align-items-center')
    time.sleep(0.5)
    # print(infs[0].text.split(" ")[0])
    # 判断交易是否存在
    if infs[0].text.split(" ")[0] != "Transaction":
        print("Transcation is not exist!")
        res.append(res_name[0])
    # print("Status:", (infs[1].text.split(':')[1]).split(' ')[0], '\n------')
    # print((infs[1].text.split(':')[1]).split(' ')[0])
    # 判断交易是否成功
    elif (infs[1].text.split(':')[1]).split(' ')[0] != "\nSuccess":
        print("Transcation is failed!")
        res.append(res_name[1])
    # 判断是否为N+2
    # print("Blocknumber:", (infs[2].text.split(':')[1]).split(' ')[0], '\n------')
    elif (infs[2].text.split(':')[1]).split(' ')[0] != ("\n"+str(logBlock+2)):
        print("Not N+2!")
        res.append(res_name[2])
    else:
        # 符合条件，获取token列表
        path = driver.find_element_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[7]/div[2]/ul")
        # print(path.text)
        lt = path.find_elements_by_xpath("li")
        time.sleep(0.5)
        # print(len(lt))
        tk_list = []
        for i in range(1, len(lt) + 1):
            try:
                tk = path.find_element_by_xpath("li[" + str(i) + "]/div/a")
                tk_list.append(tk.text)
            except Exception as err:
                print("%s" % err)

        tk_list = list(set(tk_list))
        res.append(res_name[3])
        res.append(tk_list)
    driver.close()
    return res


def get_opponent_txHash(hash):
    # 根据日志文件中的hash值得到其所在区块后一条的交易hash值，即可能对手的hash值
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/24cfcfb5548144869967d750a879ed34'))
    # print(w3.isConnected())
    data = w3.eth.get_transaction(hash)
    # print(data)
    blockNumber, transactionIndex = data.blockNumber, data.transactionIndex
    op_transaction = w3.eth.get_transaction_by_block(blockNumber, transactionIndex+1)
    # print(Web3.toHex(op_transaction.hash))
    op_hash = Web3.toHex(op_transaction.hash)
    return op_hash


def get_opponent_info(hash, token1):
    # 获取可能对手的相关信息
    # 返回值: list
    # 依次为是否抢机会(yes/no),对方botTime,对方gasPrice,对方toMiner,对方gasUsed,对方折算
    res = []
    url = 'https://etherscan.io/tx/' + hash
    # 初始化一个浏览器
    driver = webdriver.Chrome()
    driver.get(url)
    # 隐式等待
    driver.implicitly_wait(2)


    # 符合条件，获取token列表
    path = driver.find_element_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[7]/div[2]/ul")
    # print(path.text)
    lt = path.find_elements_by_xpath("li")
    print(len(lt))
    time.sleep(0.5)
    token2 = []
    for i in range(1, len(lt) + 1):
        try:
            tk = path.find_element_by_xpath("li[" + str(i) + "]/div/a")
            token2.append(tk.text)
        except Exception as err:
            print("%s" % err)

    token2 = set(token2)
    print("token2:", token2)
    token1 = set(token1)
    common = token2 & token1
    print("common", common)
    # 判断是否为抢机会
    if not common: # token列表交集为空，不是抢机会
        res.append("no")
    else: # token列表交集不为空，是抢机会
        res.append("yes")

        js = "var q=document.getElementById('collapsedLink').click()"
        driver.execute_script(js)
        time.sleep(0.5)
        infs = driver.find_elements_by_class_name('row.align-items-center')

        op_timeStamp = (infs[3].text.split('(')[1]).split(')')[0]
        res.append(op_timeStamp)
        op_gasPrice = (infs[7].text.split(':')[1]).split(' ')[0].replace('\n', '').replace(' ', '')
        res.append(op_gasPrice)
        op_toMiner = 0
        try:
            infs2 = driver.find_element_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[6]/div[2]/ul/li[1]/div")
            op_toMiner = infs2.text.split(" ")[3]
        except Exception as err:
            op_toMiner = 0
            print("%s" % err)
        op_toMiner = str(op_toMiner).replace('\n', '').replace(' ', '')
        res.append(op_toMiner)
        op_gasUsed = (infs[11].text.split(':')[1]).split(' ')[0].replace('\n', '').replace(' ', '').replace(',', '')
        res.append(op_gasUsed)
        op_gasCal = (float(op_gasPrice) * float(op_gasUsed) + float(op_toMiner)) / float(op_gasUsed)
        res.append(op_gasCal)
    driver.close()
    return res


if __name__ == '__main__':
    # df_out = info_extract()
    # res = get_status_and_token('0x03a28da6adefb0e340668c2bcefa4c47669a8e88ae36e4ea0d75744251264bde', 13006452)
    # print(res)
    # get_opponent_txHash('0x7120e417b982a97be9861ec835c8240e6c9ac08a1001355559d94483a37ed9e4')
    info_extract()
