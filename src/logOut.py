import logging
import logging.config

date = "0816"
filePath1 = '../data/' + date + '/research.csv'
filePath2 = '../data/' + date + '/gasUsed.csv'
outputPath = '../data/' + date + '/output2.csv'
logOutPath = '../data/' + date + '/logOut.log'


# 1.logging格式的配置文件
def getLogging(confName="applog"):
    logging.config.fileConfig("logging.conf")
    return logging.getLogger(confName)


logger = getLogging()


if __name__ == '__main__':
    logger = getLogging()
    logger.info("wushibniadsadas")
    logger.info("Start print log")
    logger.debug("Do something")
    logger.warning("Something maybe fail.")
    logger.info("Finish")

# # 2.编程式使用
# if __name__ == '__main__':
#     # 创建记录器
#     logger = logging.getLogger("LOGOUT")
#     logger.setLevel(logging.DEBUG)  # 默认是WARING
#     # 关于setLevel的优先级，是一个层层过滤的关系好比用网来过滤，WARNING就是网眼更大的网
#     # 先用logger的网过滤，再用handler的网过滤，最后剩下的就是输出的
#
#     # 创建处理器handler
#     consoleHandler = logging.StreamHandler()
#     # consoleHandler.setLevel(logging.DEBUG)
#
#     fileHandler = logging.FileHandler(filename=logOutPath)  # 默认使用logger的日志输出级别，可以不指定
#     # fileHandler.setLevel(logging.DEBUG)
#
#     # 创建格式化器Formatters
#     formatter = logging.Formatter("%(asctime)s | %(levelname)8s | %(filename)s [line:%(lineno)d] => %(message)s",
#                                   "%Y-%m-%d %H:%M:%S")
#
#     # 给处理器设置格式
#     consoleHandler.setFormatter(formatter)
#     fileHandler.setFormatter(formatter)
#
#     # 记录器要设置处理器
#     logger.addHandler(consoleHandler)
#     logger.addHandler(fileHandler)
#
#     # # 定义一个过滤器
#     # flt = logging.Filter("cn.cccb")  # cn.cccb开头的logger为合法
#     # # 关联过滤器
#     # logger.addFilter(flt)
#     # fileHandler.addFilter(flt)
#
#     logger.info("Start print log")
#     logger.debug("Do something")
#     logger.warning("Something maybe fail.")
#     logger.info("Finish")
# 3.字典式配置
