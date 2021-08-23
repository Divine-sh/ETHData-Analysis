import logging
import time
from web3 import Web3
from logOut import logger

infura_net = 'https://mainnet.infura.io/v3/'
project_id = '24cfcfb5548144869967d750a879ed34'
# w3 = Web3(Web3.HTTPProvider(infura_net+project_id))
# 公司内网速度更快
provider = "ws://172.17.31.104:3334"
w3 = Web3(Web3.WebsocketProvider(provider))
# print("web3 is connected: ", w3.isConnected())
connectStatus = w3.isConnected()
logger.info(f"web3 is connected:{connectStatus}")


def get_original_info(txhash, N):
    # 通过eth的api得到原交易的status、blockNumber、transactionIndex
    # 参数:
    # txHash: 原交易hash
    # N: 日志中的blockNumber
    # 根据返回值判断：
    #   ①是否存在交易
    #   ②交易是否成功
    #   ③是否为N+2
    # 返回值 res: list
    # res[0]: 不存在（not exist），失败（fail），不为N+2且不为N+1（no），为N+2符合（N+2），为N+1符合（N+1）
    # 在符合以上三个条件的情况下
    # res[1]: 对手交易的hash
    # res[2]: token1
    # res[3]: token2
    res = []
    token1 = set()
    token2 = set()
    try:
        # 获取交易实际被打包上传的块号
        origin = w3.eth.get_transaction_receipt(txhash)
        org_blockNumber = origin.blockNumber
        # 判断是否符合条件
        if origin.status == 0:  # 交易失败
            logger.info("Transaction is failed!")
            res.append("fail")
        elif org_blockNumber != (N+2) and org_blockNumber != (N+1):  # 不是N+2且不是N+1
            logger.info("Transaction is not N+1 or N+2!")
            res.append("no")
        else:  # 符合条件
            if org_blockNumber == (N+2):
                logger.info("Transaction is N+2!")
                res.append("N+2")
            else:
                logger.info("Transaction is N+1!")
                res.append("N+1")

            # 获得对手交易hash
            op_info = w3.eth.get_transaction_by_block(origin.blockNumber, origin.transactionIndex + 1)
            op_txhash = w3.toHex(op_info.hash)
            res.append(op_txhash)

            # 通过日志获得token1
            org_log = origin.logs
            for v in org_log:
                token1.add(v['address'])
            res.append(token1)
            # print(token1)

            # 同理获得token2
            op_log = w3.eth.get_transaction_receipt(op_txhash).logs
            for v in op_log:
                token2.add(v['address'])
            res.append(token2)
            # print(token2)

    except Exception as err:  # 交易不存在
        logger.info(err)
        # print("Transcation is not exist!")
        logger.info("Transcation is not exist!")
        res.append("not exist")
    finally:
        return res


def get_op_info(txhash):
    # 通过eth的api得到对手交易的status、blockNumber、transactionIndex
    # 参数:
    # txHash: 原交易hash
    # 返回值 res: list
    # res[0]: op_gasPrice
    # res[1]: op_gasUsed
    # res[2]: op_timeStamp
    res = []
    try:
        op_info1 = w3.eth.get_transaction(txhash)
        res.append(op_info1.gasPrice)
        op_info2 = w3.eth.get_transaction_receipt(txhash)
        res.append(op_info2.gasUsed)
        op_info3 = w3.eth.get_block(op_info2.blockNumber)
        # 将时间戳转换为时间元祖
        timeArray = time.localtime(op_info3.timestamp)
        # 格式化时间戳
        op_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        res.append(op_time)
    except Exception as err:
        logger.info(err)
    finally:
        return res


if __name__ == '__main__':
    # txHashs = ['0x7120e417b982a97be9861ec835c8240e6c9ac08a1001355559d94483a37ed9e4', '0x8598c0b4f55e7c09ff92ca3afdfa85d7be477ba9dcc1ce7152dd742c4acca1bc',
    #            '0xce32b23dbae12eda40110b746263ff1ee039ddfe1ff8103561e3a24fb140e9ee', '0x85136a72b62f29da3d0ea78a6f9eb91b593e9c9d125a628c0c30991323caaac2',
    #            '0x6374edde518dc1efd5a04ad1bdfa6c6ff79d0dda2e929d9543c13ba528c729ad']
    # blockNums = [13006033, 13006219, 13005907, 13006219, 13022964]
    # for i in range(len(txHashs)):
    #     res = get_original_info(txHashs[i], blockNums[i])
    #     print(res)
    # res = get_original_info('0x50c0f60db1af6b1ea341347fa2925dde7dd3d6f4c8cc6446ad22978f3c8c9ac3', 13022776)
    res = get_op_info('0x4dc6370bc292d77c1c69942f785d020a7702702167701b693c2c462b4401a17a')
    print(res)
