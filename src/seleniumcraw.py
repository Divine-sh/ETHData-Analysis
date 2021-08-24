import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from logOut import logger

base_url = 'https://etherscan.io/tx/'

# 1.firefox
# 创建一个firefoxprofie实例
firefox_profile = webdriver.FirefoxProfile()
# 开启手动设置代理
firefox_profile.set_preference('network.proxy.type', 1)
# 设置代理IP和代理端口
firefox_profile.set_preference('network.proxy.http', '127.0.0.1')
firefox_profile.set_preference('network.proxy.http_port', 7890)
# 设置https也使用该代理
firefox_profile.set_preference('network.proxy.ssl', '127.0.0.1')
firefox_profile.set_preference('network.proxy.ssl_port', 7890)
# 更新一下
firefox_profile.update_preferences()
# 创建一个options实例
firefox_options = Options()
firefox_options.add_argument('--headless')
# firefox_options.add_argument('--disable-gpu')
# firefox_options.add_argument('log-level=3')

# 2.chrome
# chrome_options = Options()
# chrome_options.add_argument('--proxy-server=http://127.0.0.1:7890')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')


def get_token_list(txhash):
    # 根据交易的hash，使用selenium爬取token列表
    # 返回值: res: list
    # token1: set
    res = []
    url = base_url + txhash
    # 初始化一个浏览器
    driver = webdriver.Firefox(firefox_profile, options=firefox_options)
    # driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    # 隐式等待
    driver.implicitly_wait(2)
    # 获取token列表
    lt = driver.find_elements_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[7]/div[2]/ul/li")
    # time.sleep(0.5)
    token = []
    for i in range(len(lt)):
        try:
            # print(lt[i].text)
            tk = lt[i].find_elements_by_tag_name('a')
            for j in range(len(tk)):
                token.append(tk[j].text)
        except Exception as err:
            logger.info(err)

    lt = driver.find_elements_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[8]/div[2]/ul/li")
    for i in range(len(lt)):
        try:
            # print(lt[i].text)
            tk = lt[i].find_elements_by_tag_name('a')
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
    driver = webdriver.Firefox(firefox_profile, options=firefox_options)
    # driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    # 隐式等待
    driver.implicitly_wait(2)
    # 获取token列表
    # path = driver.find_element_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[7]/div[2]/ul")
    # lt = path.find_elements_by_xpath("li")
    lt = driver.find_elements_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[7]/div[2]/ul/li")
    token = []
    for i in range(len(lt)):
        try:
            # print(lt[i].text)
            tk = lt[i].find_elements_by_tag_name('a')
            for j in range(len(tk)):
                token.append(tk[j].text)
        except Exception as err:
            logger.info(err)

    lt = driver.find_elements_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[8]/div[2]/ul/li")
    for i in range(len(lt)):
        try:
            # print(lt[i].text)
            tk = lt[i].find_elements_by_tag_name('a')
            for j in range(len(tk)):
                token.append(tk[j].text)
        except Exception as err:
            logger.info(err)
    res.append(set(token))

    # 获取timestamp
    infs1 = driver.find_elements_by_class_name('row.align-items-center')
    time.sleep(0.5)
    op_timeStamp = (infs1[3].text.split('(')[1]).split(')')[0]
    res.append(op_timeStamp)

    # 获取toMiner
    try:
        infs2 = driver.find_element_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[6]/div[2]/ul/li[1]/div")
        time.sleep(0.5)
        op_toMiner = infs2.text.split(" ")[3]
    except Exception as err:
        op_toMiner = 0
        logger.info(err)
    res.append(op_toMiner)
    driver.close()
    return res


def get_toMiner(txhash):
    # 根据交易的hash，使用selenium爬取交易的toMiner
    # 返回值: res: list
    # res[0]: toMiner
    res = []
    url = base_url + txhash
    # 初始化一个浏览器
    driver = webdriver.Firefox(firefox_profile, options=firefox_options)
    # driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    # 隐式等待
    driver.implicitly_wait(2)

    # 获取toMiner
    try:
        infs2 = driver.find_element_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[6]/div[2]/ul/li[1]/div")
        time.sleep(0.5)
        op_toMiner = infs2.text.split(" ")[3]
    except Exception as err:
        op_toMiner = 0
        logger.info(err)
    res.append(op_toMiner)
    driver.close()
    return res



if __name__ == '__main__':
    txhash = '0xda6cf3e946e3ddedc4c58307de36cc5f50ccc7ada6e3e57af1584026339959f9'
    print(get_token_list(txhash))
    print(get_token_list_others(txhash))