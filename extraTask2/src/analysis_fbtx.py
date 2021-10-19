from getBlockInfo import getBlockInfo, getFlashBot
from getBlockInfo import date_year, date_month, date_day
import pandas as pd
from web3 import Web3
provider = "ws://172.17.31.104:3334"
w3 = Web3(Web3.WebsocketProvider(provider))
connectStatus = w3.isConnected()
print(f"web3 is connected:{connectStatus}")
fb_data_file = f'../output/fb_data_{date_year}_{date_month}_{date_day}.csv'

def analysis_one_block(block_num, fbtx_num):
    print(f"block_num: {block_num}", fbtx_num)
    # 从 flashbot api 获取fb交易信息
    fb_info = getFlashBot(block_num)['blocks']
    # 将fb交易信息输出到明细表格中
    fb_data = pd.DataFrame(fb_info[0]['transactions'])
    # print(type(fb_data), fb_data)


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
    fbtx_info = fb_info[0]['transactions']
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
            buddle_index += 1
            sum_gasFee = 0
            sum_gasUsed = 0
            sum_gasFee += int(fbtx_info[i]['gas_price']) * int(fbtx_info[i]['gas_used'])
            sum_gasUsed += int(fbtx_info[i]['gas_used'])
    buddle_gasPrice.append(sum_gasFee/sum_gasUsed)
    print(f"buddle_index: {buddle_index}")
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

    # 新增列的值
    block_gas_price = int(fb_info[0]['gas_price'])
    fb_min_bubbleIndex = buddle_gasPrice.index(fb_min)
    fb_lastBuddle_price = buddle_gasPrice[buddle_index]
    bubble_num = buddle_index + 1
    nfb_max_series = not_fb_df[not_fb_df['equ_price'] == nfb_max]
    # print(type(nfb_max_series))
    # print(nfb_max_series)
    nfb_max_txhash = nfb_max_series['tx_hash'].values[0]
    # print(nfb_max_txhash)
    nfb_max_blockIndex = nfb_max_series['tx_index'].values[0]


    # 判断 fb 部分的交易的等效gp的最小值 是否高于 非 fb 交易部分的最大值
    if fb_lastBuddle_price >= nfb_max:
        return [[block_num, block_gas_price/1e9, fb_min/1e9, fb_min_bubbleIndex,
                fb_lastBuddle_price/1e9, 0, 0,
                bubble_num, fbtx_num, nfb_max/1e9, nfb_max_txhash, nfb_max_blockIndex,
                0, None], fb_data]
    else:
        # 新增lastbuddle在非fb交易中的位置和分位数
        nfep = not_fb_df['equ_price'].tolist()
        nfb_num = len(nfep)
        nfep.append(fb_lastBuddle_price)
        nfep.sort()
        fb_lastBuddle_position = nfep.index(fb_lastBuddle_price)
        fb_lastBuddle_quantile = '%.4f%%' % (fb_lastBuddle_position/nfb_num*100)
        print(fb_lastBuddle_position, nfb_num, fb_lastBuddle_quantile)

        # 只包含最后一个buddle的交易
        default_list = []
        for i in range(fbtx_num):
            if fbtx_info[i]['bundle_index'] == buddle_index:
                default_list.append(fbtx_info[i]['transaction_hash'])

        print(f"high-priority-transaction: {default_list}")
        return [[block_num, block_gas_price/1e9, fb_min/1e9, fb_min_bubbleIndex,
                fb_lastBuddle_price/1e9, fb_lastBuddle_position, fb_lastBuddle_quantile,
                bubble_num, fbtx_num, nfb_max/1e9, nfb_max_txhash, nfb_max_blockIndex,
                1, default_list], fb_data]


if __name__ == '__main__':
    df_out = pd.DataFrame(columns=['block_num', 'block_gas_price', 'fb_min_price', 'fb_min_buddleIndex',
                                   'fb_lastBuddle_price', 'fb_lastBuddle_position', 'fb_lastBuddle_quantile',
                                   'buddle_num', 'fbtx_num', 'nfb_max_price', 'nfb_max_txhash', 'nfb_max_blockIndex',
                                   'exist_high_priority', 'high_priority_trx'])
    block_info = getBlockInfo(5)
    for i in range(len(block_info)):
        print(f"\n第{i}个block:")
        res = analysis_one_block(int(block_info[i][0]), int(block_info[i][1]))
        if i == 0:
            res[1].to_csv(fb_data_file)
        else:
            res[1].to_csv(fb_data_file, mode='a', header=False)
        df_out.loc[i] = res[0]
        df_out.to_csv(f"../output/output_{date_year}_{date_month}_{date_day}.csv")
    df_out.to_csv(f"../output/output_{date_year}_{date_month}_{date_day}.csv")

    # analysis_one_block(13398256, 9)

