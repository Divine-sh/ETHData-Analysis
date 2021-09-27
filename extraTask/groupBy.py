import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('dataBeforeGroupBy.csv', dtype={"coinbase_transfer": str, "miner_reward": str, "NetProfit": float, "Profit": float})
    df.drop(axis=1, inplace=True, labels='index')
    print(type(df.iloc[1, 14]))
    # df0 = df[['to_address', 'finish_time']]
    # df0.columns = df0.columns.str.replace('finish_time', 'time')
    df1 = df.groupby(['to_address'])['NetProfit'].sum().reset_index(name="NetProfitSum")
    df2 = df.groupby(['to_address'])['Profit'].sum().reset_index(name="ProfitSum")
    df3 = df.groupby(['to_address'])['transaction_hash'].count().reset_index(name="trxCnt")
    df4 = pd.merge(df1, df2, on='to_address')
    df5 = pd.merge(df3, df4, on='to_address')
    df5 = df5[df5['trxCnt'] >= 24]
    df5.sort_values(by="NetProfitSum", ascending=False).head(10).to_csv("dataAfterGroupBy.csv")