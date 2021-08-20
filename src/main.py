from initial import Initial
import logging
import pandas as pd
import json
import time
from ethapi import get_original_info, get_op_info
from seleniumcraw import get_token_list, get_token_list_others
from logOut import outputPath, filePath1, filePath2, logger

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置要显示的宽度，防止轻易换行
pd.set_option('display.width', None)

logger.info(outputPath)

def data_craw(start, end):
    df, df_gasUsed, df_out = Initial(filePath1, filePath2)
    # for i in [2991, 2992]:
    for i in range(start, end):
    # for i in range(len(df)):
        # print("第%s笔交易: " % i)
        logger.info("第%s笔交易: " % i)
        # --------------------------------------------------------------------------
        # 获取日志中第i笔交易数据
        log_info = df.iloc[i, ]
        # print(log_info)
        # 得到原交易相关信息的dic
        # print("{" + log_info.msg.split('{', 1)[1])
        message = json.loads("{" + log_info.msg.split('{', 1)[1])
        # print(type(message))
        # 交易hash
        my_txHash = log_info.txHash
        # 块号
        my_blockNumber = log_info.blockNumber
        # 格式化我方时间时间戳
        timeArray = time.localtime(log_info.logTime)
        my_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # 我方gasPrice
        my_gasPrice = message['results'][1]['gasPrice']
        # 我方toMiner
        # my_toMiner = int(message['_ethAmountToCoinbase']['hex'], 16)
        my_toMiner = 0
        # 查找我方gasUsed
        df_GU = df_gasUsed[df_gasUsed['txHash'] == log_info.txHash]
        if df_GU.empty:
            my_gasUsed = 1
        else:
            my_gasUsed = df_gasUsed[df_gasUsed['txHash'] == log_info.txHash].iloc[0, 1]
        # 我方折算
        my_gasCal = float(int(my_gasPrice) * int(my_gasUsed) + int(my_toMiner)) / my_gasUsed
        # print(my_gasCal)
        # --------------------------------------------------------------------------
        # 通过eth的api得到原交易的status、blockNumber、transactionIndex
        # 并判断: ①是否存在交易 ②交易是否成功 ③是否为N+2
        # 都满足时返回对手交易的hash
        result1 = get_original_info(my_txHash, my_blockNumber)
        # print(result1)
        if result1[0] != "yes":  # 不满足三个条件，直接跳过
            df_out.loc[i] = [my_txHash, my_blockNumber, my_time, my_gasPrice, my_toMiner, my_gasUsed, my_gasCal, result1[0], "no", None, None, None, None, None]
        else:  # 满足三个条件，判断是否是抢交易
            op_hash = result1[1]
            org_res, op_res = get_token_list(my_txHash), get_token_list_others(op_hash)
            op_timeStamp, op_toMiner = op_res[1], op_res[2]
            token1, token2 = org_res[0], op_res[0]
            # print("token1:", token1, "token2:", token2)
            logger.info(f"token1:{token1}")
            logger.info(f"token2:{token2}")
            common = token1 & token2
            # 判断是否为抢机会
            if not common:  # token列表交集为空，不是抢机会
                # print("Not opponent!")
                logger.info("Not opponent!")
                df_out.loc[i] = [my_txHash, my_blockNumber, my_time, my_gasPrice, my_toMiner, my_gasUsed, my_gasCal, result1[0], "no", None, None, None, None, None]
            else:  # token列表交集不为空，是抢机会
                # print("Opponent!")
                logger.info("Opponent!")
                op_info = get_op_info(op_hash)
                op_gasPrice, op_gasUsed = op_info[0], op_info[1]
                # op_gasPrice, op_gasUsed = result1[2], result1[3]
                # print("op_gasPrice:", op_gasPrice, "op_gasUsed:", op_gasUsed, "op_toMiner:", op_toMiner)
                op_gasCal = (op_gasPrice * op_gasUsed + float(op_toMiner)) / op_gasUsed
                df_out.loc[i] = [my_txHash, my_blockNumber, my_time, my_gasPrice, my_toMiner, my_gasUsed, my_gasCal, result1[0], "yes", op_timeStamp, op_gasPrice, op_toMiner, op_gasUsed, op_gasCal]
        # df_out.to_csv(outputPath, encoding="utf_8_sig")
    print(df_out)
    # 输出到csv文件
    df_out.to_csv(outputPath, encoding="utf_8_sig", mode='a', header=False) #


if __name__ == '__main__':
    start = 1782
    end = 1808
    data_craw(start, end)
