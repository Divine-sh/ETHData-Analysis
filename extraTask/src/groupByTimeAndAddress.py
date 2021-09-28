import pandas as pd
import datetime

if __name__ == '__main__':
    df = pd.read_csv('../input/dataBeforeGroupBy.csv',
                     dtype={"coinbase_transfer": str, "miner_reward": str, "NetProfit": float, "Profit": float, "finish_time": str})

    df.drop(axis=1, inplace=True, labels='index')
    for i in range(0, len(df)):
        df.iloc[i, 11] = datetime.datetime.strptime(df.iloc[i, 11], "%Y-%m-%d  %H:%M")

    df1 = df.groupby(['to_address', pd.Grouper(freq='1D', key='finish_time')]).agg({'NetProfit': 'sum', 'Profit': 'sum'})  # [["NetProfit", "Profit"]].sum()
    df2 = df.groupby(['to_address', pd.Grouper(freq='1D', key='finish_time')])["transaction_hash"].count()
    df3 = pd.merge(df1, df2, on=['to_address', 'finish_time'])
    # print(df3.index)
    df3.rename(columns={'finish_time': 'time', 'NetProfit': 'NetProfitSum',
                        'Profit': 'ProfitSum', 'transaction_hash': 'txCnt'}, inplace=True)
    # df3 = df3[df3['txCnt'] >= 24]
    # df3.sort_values(by='NetProfitSum', ascending=False).head(10).to_csv("dataAfterGroupBy.csv")
    df3.sort_values(by='NetProfitSum', ascending=False).to_csv("../output/dataAfterGroupByTimeAndAddress.csv")