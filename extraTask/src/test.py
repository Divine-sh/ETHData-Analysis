import datetime
import pandas as pd
# a = '2021/9/18  18:58:00'
# print(a)
# b = datetime.datetime.strptime(str(a), "%Y/%m/%d  %H:%M:%S")
# print(b)

if __name__ == '__main__':
    df = pd.read_csv('dataBeforeGroupBy.csv',
                     dtype={"coinbase_transfer": str, "miner_reward": str, "NetProfit": float, "Profit": float})
    df.drop(axis=1, inplace=True, labels='index')
    print(len(df))
    for i in range(0, len(df)):
        df.iloc[i, 11] = datetime.datetime.strptime(df.iloc[i, 11], "%Y-%m-%d  %H:%M")
        # print(df.iloc[i, 11])
    df.to_csv("dataBeforeGroupBy2.csv")