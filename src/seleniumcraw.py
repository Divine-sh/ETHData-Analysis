import logging
import time
from selenium import webdriver
from logOut import logger

base_url = 'https://etherscan.io/tx/'
chromeOptions = webdriver.ChromeOptions()
# 设置代理,注意等号两边不能有空格(直接本地ip加连接clash的端口即可)
chromeOptions.add_argument("--proxy-server=http://127.0.0.1:7890")
# # 静默模式，后台运行
# chromeOptions.add_argument('--headless')
# chromeOptions.add_argument('--disable-gpu')


def get_token_list(txhash):
    # 根据交易的hash，使用selenium爬取token列表
    # 返回值: res: list
    # token1: set
    res = []
    url = base_url + txhash
    # 初始化一个浏览器
    driver = webdriver.Chrome(options=chromeOptions)
    driver.get(url)
    # 隐式等待
    # driver.implicitly_wait(1)
    # 获取token列表
    lt = driver.find_elements_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[7]/div[2]/ul/li")
    # time.sleep(0.5)
    token = []
    for i in range(len(lt)):
        try:
            # print(lt[i].text)
            tk = lt[i].find_elements_by_tag_name('a')
            # print(tk.text)
            for j in range(len(tk)):
                token.append(tk[j].text)
        except Exception as err:
            logger.info(err)

    lt = driver.find_elements_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[8]/div[2]/ul/li")
    # time.sleep(0.5)
    for i in range(len(lt)):
        try:
            # print(lt[i].text)
            tk = lt[i].find_elements_by_tag_name('a')
            # print(tk.text)
            for j in range(len(tk)):
                token.append(tk[j].text)
        except Exception as err:
            logger.info(err)
    res.append(set(token))

    driver.close()
    return res



def get_token_list_others(txhash):
    # 根据交易的hash，使用selenium爬取token列表，others: timestamp和toMiner
    # 返回值: res: list
    # token2: set
    # timestamp
    # toMiner
    res = []
    url = base_url + txhash
    # 初始化一个浏览器
    driver = webdriver.Chrome(options=chromeOptions)
    driver.get(url)
    # 隐式等待
    # driver.implicitly_wait(1)
    # 获取token列表
    # path = driver.find_element_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[7]/div[2]/ul")
    # lt = path.find_elements_by_xpath("li")
    lt = driver.find_elements_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[7]/div[2]/ul/li")
    # time.sleep(0.5)
    token = []
    for i in range(len(lt)):
        try:
            # print(lt[i].text)
            tk = lt[i].find_elements_by_tag_name('a')
            # print(tk.text)
            for j in range(len(tk)):
                token.append(tk[j].text)
        except Exception as err:
            logger.info(err)

    lt = driver.find_elements_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[8]/div[2]/ul/li")
    for i in range(len(lt)):
        try:
            # print(lt[i].text)
            tk = lt[i].find_elements_by_tag_name('a')
            # print(tk.text)
            for j in range(len(tk)):
                token.append(tk[j].text)
        except Exception as err:
            logger.info(err)
    res.append(set(token))

    # 获取timestamp
    infs1 = driver.find_elements_by_class_name('row.align-items-center')

    op_timeStamp = (infs1[3].text.split('(')[1]).split(')')[0]
    res.append(op_timeStamp)

    # 获取toMiner
    try:
        infs2 = driver.find_element_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[6]/div[2]/ul/li[1]/div")
        op_toMiner = infs2.text.split(" ")[3]
    except Exception as err:
        op_toMiner = 0
        logger.info(err)
    res.append(op_toMiner)
    driver.close()
    return res


if __name__ == '__main__':
    txhash = '0x69ca2a69db90a7d80daf2a37c3ffb3f6a1bfdd9dc97ddd5115f722c2ec441486'
    print(get_token_list(txhash))
    # print(get_token_list_others(txhash))