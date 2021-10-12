from getBlockInfo import getBlockInfo
import pandas as pd
from web3 import Web3
provider = "ws://172.17.31.104:3334"
w3 = Web3(Web3.WebsocketProvider(provider))
connectStatus = w3.isConnected()
print(f"web3 is connected:{connectStatus}")


def analysis_one_block(block_num, fbtx_num):
    print(block_num, fbtx_num)
    df = pd.DataFrame(columns=('tx_index', 'tx_hash', 'gas_price', 'equ_price'))
    block_len = len(w3.eth.get_block(block_num).transactions)
    print("block_len: ", block_len)
    baseGP = w3.eth.get_block(block_num).baseFeePerGas

    # 计算所有交易的等价gasPrice
    for i in range(block_len):
        res1 = w3.eth.get_transaction_by_block(block_num, i)
        # print(res1.hash.hex(), res1.gasPrice)
        equ_price = res1.gasPrice - baseGP
        # print(equ_price)
        df.loc[i] = [i, res1.hash.hex(), res1.gasPrice, equ_price]
    # print(df)
    fb_df = df.iloc[0:fbtx_num]
    # print(fb_df)
    not_fb_df = df.iloc[fbtx_num:]
    # print(not_fb_df)
    fb_min = fb_df.min().equ_price
    nfb_max = not_fb_df.max().equ_price
    print(fb_min, nfb_max)
    # 判断 fb 部分的交易的等效gp的最小值 是否高于 非 fb 交易部分的最大值
    if fb_min >= nfb_max:
        return [block_num, fb_min, nfb_max, 0, None]
    else:
        default_list = []
        default_df = fb_df[fb_df['equ_price'] < nfb_max]
        # print(default_df)
        # print(type(default_df))
        for v in default_df['tx_hash']:
            default_list.append(v)
        return [block_num, fb_min, nfb_max, 1, default_list]


if __name__ == '__main__':
    df_out = pd.DataFrame(columns=['block_num', 'fb_min', 'nfb_max', 'exist_high_priority', 'high_priority_account'])
    block_info = getBlockInfo(50)
    # for i in range(len(block_info)):
    #     res = analysis_one_block(int(block_info[i][0]), int(block_info[i][1]))
    #     df_out.loc[i] = res
    # df_out.to_csv("output.csv")
    analysis_one_block(13398252, 3)