import logging

from web3 import Web3
from logOut import logger

infura_net = 'https://mainnet.infura.io/v3/'
project_id = '24cfcfb5548144869967d750a879ed34'
w3 = Web3(Web3.HTTPProvider(infura_net + project_id))
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
    # 首位: 不存在（not exist），失败（fail），不为N+2（no），符合（yes）
    # 对手交易的hash: 符合三个条件的情况下
    # xx对手交易的gasPricexx
    # xx对手交易的gasUsedxx
    res = []
    try:
        origin = w3.eth.get_transaction_receipt(txhash)
        # print(origin)
        if origin.status == 0:  # 交易失败
            # print("Transaction is failed!")
            logger.info("Transaction is failed!")
            res.append("fail")
        elif origin.blockNumber != (N+2): # 不是N+2
            # print("Transaction is not N+2!")
            logger.info("Transaction is not N+2!")
            res.append("no")
        else:  # 符合条件
            # 获得对手交易hash
            op_info = w3.eth.get_transaction_by_block(origin.blockNumber, origin.transactionIndex + 1)
            res.append("yes")
            res.append(w3.toHex(op_info.hash))
            # res.append(op_info.gasPrice)
            # op_info2 = w3.eth.get_transaction_receipt(w3.toHex(op_info.hash))
            # res.append(op_info2.gasUsed)
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
    # op_gasPrice、gasUsed
    res = []
    try:
        op_info1 = w3.eth.get_transaction(txhash)
        res.append(op_info1.gasPrice)
        op_info2 = w3.eth.get_transaction_receipt(txhash)
        res.append(op_info2.gasUsed)
    except Exception as err:
        logger.info(err)
    finally:
        return res


if __name__ == '__main__':
    txHashs = ['0x7120e417b982a97be9861ec835c8240e6c9ac08a1001355559d94483a37ed9e4', '0x8598c0b4f55e7c09ff92ca3afdfa85d7be477ba9dcc1ce7152dd742c4acca1bc',
               '0xce32b23dbae12eda40110b746263ff1ee039ddfe1ff8103561e3a24fb140e9ee', '0x85136a72b62f29da3d0ea78a6f9eb91b593e9c9d125a628c0c30991323caaac2']
    blockNums = [13006033, 13006219, 13005907, 13006219]
    for i in range(len(txHashs)):
        res = get_original_info(txHashs[i], blockNums[i])
        print(res)
