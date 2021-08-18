from initial import Initial
import pandas as pd
import json
import time
from ethapi import get_original_info, get_op_info
from seleniumcraw import get_token_list, get_token_list_others

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置要显示的宽度，防止轻易换行
pd.set_option('display.width', None)

date = "0816"
filePath1 = '../data/' + date + '/research.csv'
filePath2 = '../data/' + date + '/gasUsed.csv'
outputPath = '../data/' + date + '/output.csv'
print(outputPath)

if __name__ == '__main__':
    df, df_gasUsed, df_out = Initial(filePath1, filePath2)
    # for i in [34, 49, 75, 81]:
    for i in range(len(df)):
        print("第%s笔交易: " % i)
        # --------------------------------------------------------------------------
        # 获取日志中第i笔交易数据
        log_info = df.iloc[i, ]
        start = len("final contract params are ,")
        # 得到原交易相关信息的dic
        message = json.loads(log_info.msg[start:])
        # 格式化我方时间时间戳
        timeArray = time.localtime(log_info.logTime)
        my_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # 我方gasPrice
        my_gasPrice = int(message['overrides']['maxFeePerGas']['hex'], 16)
        # 我方toMiner
        my_toMiner = int(message['_ethAmountToCoinbase']['hex'], 16)
        # 查找我方gasUsed
        df_GU = df_gasUsed[df_gasUsed['txHash'] == log_info.txHash]
        if df_GU.empty:
            my_gasUsed = 1
        else:
            my_gasUsed = df_gasUsed[df_gasUsed['txHash'] == log_info.txHash].iloc[0, 1]
        # 我方折算
        my_gasCal = (my_gasPrice * my_gasUsed + my_toMiner) / my_gasUsed
        # --------------------------------------------------------------------------
        # 通过eth的api得到原交易的status、blockNumber、transactionIndex
        # 并判断: ①是否存在交易 ②交易是否成功 ③是否为N+2
        # 都满足时返回对手交易的hash
        result1 = get_original_info(log_info.txHash, log_info.blockNumber)
        # print(result1)
        if result1[0] != "yes":  # 不满足三个条件，直接跳过
            df_out.loc[i] = [log_info.txHash, log_info.blockNumber, my_time, my_gasPrice, my_toMiner, my_gasUsed, my_gasCal, result1[0], "no", None, None, None, None, None]
            continue
        else:  # 满足三个条件，判断是否是抢交易
            op_hash = result1[1]
            org_res, op_res = get_token_list(log_info.txHash), get_token_list_others(op_hash)
            op_timeStamp, op_toMiner = op_res[1], op_res[2]
            token1, token2 = org_res[0], op_res[0]
            print("token1:", token1, "token2:", token2)
            common = token1 & token2
            # 判断是否为抢机会
            if not common:  # token列表交集为空，不是抢机会
                print("Not opponent!")
                df_out.loc[i] = [log_info.txHash, log_info.blockNumber, my_time, my_gasPrice, my_toMiner, my_gasUsed, my_gasCal, result1[0], "no", None, None, None, None, None]
            else:  # token列表交集不为空，是抢机会
                print("Opponent!")
                op_info = get_op_info(op_hash)
                op_gasPrice, op_gasUsed = op_info[0], op_info[1]
                # op_gasPrice, op_gasUsed = result1[2], result1[3]
                # print("op_gasPrice:", op_gasPrice, "op_gasUsed:", op_gasUsed, "op_toMiner:", op_toMiner)
                op_gasCal = (op_gasPrice * op_gasUsed + float(op_toMiner)) / op_gasUsed
                df_out.loc[i] = [log_info.txHash, log_info.blockNumber, my_time, my_gasPrice, my_toMiner, my_gasUsed, my_gasCal, result1[0], "yes", op_timeStamp, op_gasPrice, op_toMiner, op_gasUsed, op_gasCal]
    print(df_out)
    # 输出到csv文件
    df_out.to_csv(outputPath, encoding="utf_8_sig")
