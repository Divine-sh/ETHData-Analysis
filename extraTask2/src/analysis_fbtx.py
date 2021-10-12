from getBlockInfo import getBlockInfo
# #
# for v in block_info:
#     block_num = int(v[0])
#     tx_index = int(v[1])
#     baseGP = int(v[2])
#     print(block_num, tx_index, baseGP)
#     # 得到一个块中的
#     for i in range(tx_index):
#         res = w3.eth.get_transaction_by_block(block_num, i)
#         print(res)
#         if i == 0:
#             minGP = res.gasPrice
#         else:
#             minGP = min(minGP, res.gasPrice)
#     print(w3.eth.get_block(12073898))

if __name__ == '__main__':
    block_info = getBlockInfo(1)