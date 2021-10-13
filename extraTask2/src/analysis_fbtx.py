from getBlockInfo import getBlockInfo,getFlashBot
import pandas as pd
from web3 import Web3
provider = "ws://172.17.31.104:3334"
w3 = Web3(Web3.WebsocketProvider(provider))
connectStatus = w3.isConnected()
print(f"web3 is connected:{connectStatus}")


def analysis_one_block(block_num, fbtx_num):
    print(f"block_num: {block_num}", fbtx_num)
    # 从 flashbot api 获取fb交易信息
    fb_info = getFlashBot(block_num)
    df = pd.DataFrame(columns=('tx_index', 'tx_hash', 'gas_price', 'equ_price'))
    block_len = len(w3.eth.get_block(block_num).transactions)
    # print(w3.eth.get_block(block_num).transactions)
    print(f"block_len: {block_len}")
    baseGP = w3.eth.get_block(block_num).baseFeePerGas

    # 计算所有交易的等价gasPrice
    for i in range(block_len):
        res1 = w3.eth.get_transaction_by_block(block_num, i)
        # print(res1.hash.hex(), res1.gasPrice)
        equ_price = res1.gasPrice - baseGP
        # print(equ_price)
        df.loc[i] = [i, res1.hash.hex(), res1.gasPrice, equ_price]

    # fb交易存在buddle交易，及多笔交易互为伙伴交易，这时候这些交易需要计算一个buddle_gas_price
    # 计算fb交易的buddle_price并计算fb的最小等效gasPrice
    fbtx_info = fb_info['blocks'][0]['transactions']
    buddle_index = 0
    sum_gasFee = 0
    sum_gasUsed = 0
    buddle_gasPrice = []
    for i in range(len(fbtx_info)):
        if fbtx_info[i]['bundle_index'] == buddle_index:
            sum_gasFee += int(fbtx_info[i]['gas_price']) * int(fbtx_info[i]['gas_used'])
            sum_gasUsed += int(fbtx_info[i]['gas_used'])
        else:
            buddle_gasPrice.append(sum_gasFee/sum_gasUsed)
            sum_gasFee = 0
            sum_gasUsed = 0
            buddle_index += 1
            sum_gasFee += int(fbtx_info[i]['gas_price']) * int(fbtx_info[i]['gas_used'])
            sum_gasUsed += int(fbtx_info[i]['gas_used'])
    buddle_gasPrice.append(sum_gasFee / sum_gasUsed)
    print(f"buddle_gasPrice: {buddle_gasPrice}")
    fb_min = min(buddle_gasPrice)
    print(f"fb_min: {fb_min}")

    # 计算非fb交易的最大等效gasPrice
    not_fb_df = df.iloc[fbtx_num:]
    nfb_max = not_fb_df.max().equ_price
    print(f"nfb_max: {nfb_max}")

    # 向fb_df中新增一列buddle_price
    fb_df = df.iloc[0:fbtx_num]
    fb_df = fb_df.copy()
    fb_df['buddle_price'] = ''
    # print(fb_df)
    for i in range(fbtx_num):
        fb_df = fb_df.copy()
        fb_df.loc[i, ['buddle_price']] = buddle_gasPrice[fbtx_info[i]['bundle_index']]
    # print(fb_df)

    # 判断 fb 部分的交易的等效gp的最小值 是否高于 非 fb 交易部分的最大值
    if fb_min >= nfb_max:
        return [block_num, fb_min, nfb_max, 0, None]
    else:
        default_list = []
        default_df = fb_df[fb_df['buddle_price'] < nfb_max]
        # print(default_df)
        # print(type(default_df))
        for v in default_df['tx_hash']:
            default_list.append(v)
        print(f"high-priority-transaction: {default_list}")
        return [block_num, fb_min, nfb_max, 1, default_list]


if __name__ == '__main__':
    df_out = pd.DataFrame(columns=['block_num', 'fb_min', 'nfb_max', 'exist_high_priority', 'high_priority_account'])
    block_info = getBlockInfo(1000)
    for i in range(len(block_info)):
        print(f"\n第{i}个block:")
        res = analysis_one_block(int(block_info[i][0]), int(block_info[i][1]))
        df_out.loc[i] = res
        df_out.to_csv("../output/output1000.csv")
    df_out.to_csv("../output/output1000.csv")

    # analysis_one_block(13398256, 9)