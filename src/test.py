# import pandas as pd
#
#
# a = pd.DataFrame({'a': [1, 2, 3], 'b': [2, 3, 4]})
# b = pd.DataFrame({'a': [1, 2, 3], 'b': [22, 33, 44]})
# a.loc[7] = [7, 7]
# a.loc[4] = [4, 4]
# print(pd.concat([a, b]))
#
# df_out = pd.DataFrame(columns=('a', 'b'))
# print(df_out)
# df_out.loc[2] = [8, 8]
# print(df_out)
#
# date = "0816"
# filePath1 = '../data/' + date + '/research.csv'
# filePath2 = '../data/' + date + '/gasUsed.csv'
# outputPath = '../data/' + date + '/output.csv'
# print(outputPath)
import logging

logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='../data/' + date + '/logOut.log',
                    # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志,a是追加模式，默认如果不写的话，就是追加模式
                    filemode='a',
                    # 日志格式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )
logging.info("Start print log")
logging.debug("Do something")
logging.warning("Something maybe fail.")
logging.info("Finish")
