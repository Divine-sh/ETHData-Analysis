import pandas as pd
import time
from web3 import Web3

# # 通过infura连接
# infura_net = 'https://mainnet.infura.io/v3/'
# project_id = '24cfcfb5548144869967d750a879ed34'
# w3 = Web3(Web3.HTTPProvider(infura_net+project_id))
# 公司内网速度更快
provider = "ws://172.17.31.104:3334"
w3 = Web3(Web3.WebsocketProvider(provider))
connectStatus = w3.isConnected()
print(f"web3 is connected:{connectStatus}")
# 文件名
fileName = '423494_2021_09_22.csv'
inName = 'arbitrageTrx.csv'
outName = 'output.csv'


def Initial(filePath):
    # 读取csv文件
    # df = pd.read_csv(filePath, usecols=[0, 4, 5, 6, 7, 11], dtype={"coinbase_transfer": str})
    df = pd.read_csv(filePath, dtype={"coinbase_transfer": str, "miner_reward": str})
    print(f"The amount of transaction is: {len(df)}\n")
    # # 去重
    # # 去重列，按这些列进行去重
    # # 保存第一条重复数据
    # df.drop_duplicates(subset=['transaction_hash'],  keep='first', inplace=True)
    # print(f"The de-duplication amount of transaction is: {len(df)}")
    return df


def isArbitrage(txHash):
    trx_rep = w3.eth.get_transaction_receipt(txHash)
    # print(trx_rep)
    # 获取交易日志
    trx_log = trx_rep.logs
    # 分析日志，首先根据topics筛选出为transfer的交易
    # 有两笔以上transfer交易且第一笔和最后一笔都为WETH的符合条件
    transfer_list = []
    for log in trx_log:
        topic = log.topics[0].hex()
        if topic == '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef':
            transfer_list.append(log.address.lower())
    # print(transfer_list)
    tl_len = len(transfer_list)
    if tl_len > 2 and transfer_list[0] == transfer_list[tl_len - 1] == '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2':
        return True
    else:
        return False


def dataClean(dataframe):
    print(f"The amount of transaction before cleaning is: {len(dataframe)}\n")
    dataframe['isArbitrage'] = False
    # print(txHash)
    for i in range(0, len(dataframe)):
        trx_info = dataframe.iloc[i]
        txHash = trx_info['transaction_hash']
        print(f"<{i}> transaction hash is: ", txHash)
        # txHash = '0xb9026f856a9a4dfb9ab970015f75b10a582560fdebe33a87e9296880f623a7b3'
        dataframe.iloc[i, 12] = isArbitrage(txHash)
    dataframe = dataframe[dataframe['isArbitrage'] == True]
    print(f"The amount of transaction after cleaning is: {len(dataframe)}\n")
    dataframe.to_csv('arbitrageTrx.csv')
    return dataframe


if __name__ == '__main__':
    df = Initial(inName)
    # 插入
    df['NetProfit'] = '-1'
    df['Profit'] = '-2'
    for i in range(0, len(df)):
        trx_info = df.iloc[i]
        txHash = trx_info['transaction_hash']
        print(f"<{i}> transaction hash is: ", txHash)
        trx_chain = w3.eth.get_transaction(txHash)
        # 都为int类型
        gasFee = trx_chain['gasPrice'] * trx_info['gas_used']
        # print(gasFee)
        transferToMiner = trx_info['coinbase_transfer']
        # print(transferToMiner)
        Cost = gasFee + int(transferToMiner)
        # print(Cost)
        trx_rep = w3.eth.get_transaction_receipt(txHash)
        trx_log = trx_rep.logs
        tsf_list = []
        for log in trx_log:
            topic = log.topics[0].hex()
            if topic == '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef':
                tsf_list.append(log)
        # print(int(tsf_list[0].input, 16))
        # print(int(tsf_list[-1].input, 16))
        Profit = int(tsf_list[-1].data, 16) - int(tsf_list[0].data, 16)
        print("利润", Profit)
        NetProfit = Profit - Cost
        print("净利润", NetProfit)
        df.iloc[i, 14] = NetProfit
        df.iloc[i, 15] = Profit
    df.to_csv('dataBeforeGroupBy.csv')


