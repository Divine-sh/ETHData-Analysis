import pandas as pd

fileName = '423494_2021_09_22.csv'


def Initial(filePath):
    # 读取csv文件
    df = pd.read_csv(filePath, usecols='transaction_hash')
    print(f"The amount of transaction is: {len(df)}")
    # 去重
    # 去重列，按这些列进行去重
    # 保存第一条重复数据
    df.drop_duplicates(subset=['txHash'],  keep='first', inplace=True)
    print(f"The de-duplication amount of transaction is: {len(df)}")
    return df


if __name__ == '__main__':
    Initial(fileName)