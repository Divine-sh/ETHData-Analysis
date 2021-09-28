import pandas as pd
import datetime

if __name__ == '__main__':
    df = pd.read_csv('dataBeforeGroupBy.csv',
                     dtype={"coinbase_transfer": str, "miner_reward": str, "NetProfit": float, "Profit": float, "finish_time": str})

    df.drop(axis=1, inplace=True, labels='index')

    df1 = df.groupby(['to_address'])[["NetProfit", "Profit"]].sum()
    df2 = df.groupby(['to_address'])["transaction_hash"].count()
    df3 = pd.merge(df1, df2, on=['to_address'])
    df3.rename(columns={'NetProfit': 'NetProfitSum', 'Profit': 'ProfitSum', 'transaction_hash': 'txCnt'}, inplace=True)
    df3 = df3[df3['txCnt'] >= 24]
    # df3.sort_values(by='NetProfitSum', ascending=False).head(10).to_csv("dataAfterGroupBy.csv")
    df3.sort_values(by='NetProfitSum', ascending=False).head(10).to_csv("dataAfterGroupByAddress.csv")