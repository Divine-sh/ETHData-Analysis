import logging

import pandas as pd
from logOut import logger


def Initial(filepath1, filepath2):
    # 读取csv文件
    df = pd.read_csv(filepath1)
    # print("The amount of transaction is: ", len(df))
    logger.info(f"The initial amount of transaction is: {len(df)}")
    # 去重
    # 去重列，按这些列进行去重
    # 保存第一条重复数据
    df.drop_duplicates(subset=['txHash'],  keep='first', inplace=True)
    logger.info(f"The de-duplication amount of transaction is: {len(df)}")

    df_gasUsed = pd.read_csv(filepath2)
    c1 = ("txHash", "blockNumber", "我方time", "我方gasPrice", "我方toMiner", "我方gasUsed", "我方折算")
    c2 = ("是否N+2", "是否抢机会", "对方txHash", "对方botTime", "对方gasPrice", "对方toMiner", "对方gasUsed", "对方折算")
    df_out = pd.DataFrame(columns=c1+c2)
    return df, df_gasUsed, df_out


if __name__ == '__main__':
    Initial('../data/0816/research.csv', '../data/0816/gasUsed.csv')
