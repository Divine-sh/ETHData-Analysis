from selenium import webdriver
import time

base_url = 'https://etherscan.io/tx/'
chromeOptions = webdriver.ChromeOptions()
# 设置代理,注意等号两边不能有空格(直接本地ip加连接clash的端口即可)
chromeOptions.add_argument("--proxy-server=http://127.0.0.1:7890")


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
    driver.implicitly_wait(1)
    # 获取token列表
    lt = driver.find_elements_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[7]/div[2]/ul/li")
    time.sleep(0.5)
    token2 = []
    for i in range(0, len(lt)):
        try:
            # print(lt[i].text)
            tk = lt[i].find_element_by_tag_name('a')
            # print(tk.text)
            token2.append(tk.text)
        except Exception as err:
            print("%s" % err)
    res.append(set(token2))

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
    driver.implicitly_wait(1)
    # 获取token列表
    # path = driver.find_element_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[7]/div[2]/ul")
    # lt = path.find_elements_by_xpath("li")
    lt = driver.find_elements_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[7]/div[2]/ul/li")
    time.sleep(0.5)
    token2 = []
    for i in range(0, len(lt)):
        try:
            # print(lt[i].text)
            tk = lt[i].find_element_by_tag_name('a')
            # print(tk.text)
            token2.append(tk.text)
        except Exception as err:
            print("%s" % err)
    res.append(set(token2))

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
        print("%s" % err)
    res.append(op_toMiner)
    driver.close()
    return res


if __name__ == '__main__':
    txhash = '0x7120e417b982a97be9861ec835c8240e6c9ac08a1001355559d94483a37ed9e4'
    print(get_token_list(txhash))
    print(get_token_list_others(txhash))