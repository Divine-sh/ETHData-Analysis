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

def Initial(filePath):
    # 读取csv文件
    df = pd.read_csv(filePath, usecols=[0, 4, 5, 6, 7, 11], dtype={"coinbase_transfer": str})
    print(f"The amount of transaction is: {len(df)}\n")
    # # 去重
    # # 去重列，按这些列进行去重
    # # 保存第一条重复数据
    # df.drop_duplicates(subset=['transaction_hash'],  keep='first', inplace=True)
    # print(f"The de-duplication amount of transaction is: {len(df)}")
    return df

def isArbitrage(txHash):
    trx_rep = w3.eth.get_transaction_receipt(txHash)
    print(trx_rep)
    # 获取交易日志
    trx_log = trx_rep.logs
    # 分析日志，首先根据topics筛选出为transfer的交易
    # 有两笔以上transfer交易且第一笔和最后一笔都为WETH的符合条件
    transfer_list = []
    for log in trx_log:
        topic = log.topics[0].hex()
        # print(type(topic), topic)
        if topic == '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef':
            # print(log.address.lower())
            transfer_list.append(log.address.lower())
    print(transfer_list)
    tl_len = len(transfer_list)
    if tl_len > 2 and transfer_list[0] == transfer_list[tl_len - 1] == '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2':
        return True
    else:
        return False


if __name__ == '__main__':
    txHash = Initial(fileName)
    # print(txHash)
    for i in range(0, 1):
        trx = txHash.iloc[i]
        print(f"<{i}> transaction hash is: ", trx['transaction_hash'])
        # tx = '0xb9026f856a9a4dfb9ab970015f75b10a582560fdebe33a87e9296880f623a7b3'
        if isArbitrage(trx['transaction_hash']):
            # print(type(trx['gas_used']), trx['gas_used'])
            gasFee = trx['gas_used']*trx['gas_price']
            transferToMiner = trx['coinbase_transfer']
            Cost = gasFee + int(transferToMiner)