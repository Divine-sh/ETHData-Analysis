from selenium import webdriver
from selenium.webdriver.firefox.options import Options

base_url = 'https://etherscan.io/tx/'
profile = webdriver.FirefoxProfile()
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.http', '127.0.0.1')
profile.set_preference('network.proxy.http_port', 7890)
profile.set_preference('network.proxy.ssl', '127.0.0.1')
profile.set_preference('network.proxy.ssl_port', 7890)
profile.update_preferences()

options = Options()
options.add_argument('-headless')
# options.add_argument('--disable-gpu')
# options.add_argument('log-level=3')


def get_token_list(txhash):
    # 根据交易的hash，使用selenium爬取token列表
    # 返回值: res: list
    # token1: set
    res = []
    url = base_url + txhash
    print(url)
    # 初始化一个浏览器
    driver = webdriver.Firefox(profile, options=options)

    driver.get(url)
    # 隐式等待
    # driver.implicitly_wait(2)
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
            print(err)

    lt = driver.find_elements_by_xpath("//*[@id=\"ContentPlaceHolder1_maintable\"]/div[8]/div[2]/ul/li")
    for i in range(len(lt)):
        try:
            # print(lt[i].text)
            tk = lt[i].find_elements_by_tag_name('a')
            for j in range(len(tk)):
                token.append(tk[j].text)
        except Exception as err:
            print(err)
    res.append(set(token))
    print(token)
    driver.close()
    return res



if __name__ == '__main__':
    txhash = '0xda6cf3e946e3ddedc4c58307de36cc5f50ccc7ada6e3e57af1584026339959f9'
    print(get_token_list(txhash))



