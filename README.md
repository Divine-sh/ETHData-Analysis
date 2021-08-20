## 文件结构：

### src/

main.py：main文件，程序主流程

initial.py：前期读取csv文件和构造df_out

ethapi.py：包含使用eth的接口的函数

seleniumcraw.py：包含使用selenium爬取的函数

logOut.py：包含提供日志输出的logger实例

logging.conf：logging模块的配置文件

#### data/date

date：数据对应日期

reasearch.csv、gasUsed.csv：输入文件

output.csv： 输出文件 (输入数据很大时可能切片输出1,2,3,4,5...)

## 程序流程：

### 前期处理：

读取research和gasUsed的csv文件得到df；
构造df_out；

### 遍历df，进行分析和数据爬取：

1.通过eth的api得到原交易的status、blockNumber、transactionIndex

​	**web3.eth.get_transaction_receipt(txHash)**

​	根据返回值判断：

​		①是否存在交易

​		②交易是否成功

​		③是否为N+2

​	以上条件都成立时，通过

​	**web3.eth.get_transaction_by_block(blockNumber,Index)**

​	得到可能存在的对手的交易hash

2.通过原交易和对手交易的hash，用selenium爬取token列表（对于对手交易，顺便获取op_timeStamp和op_toMiner），判断是否为抢交易：

​	若是抢交易，再通过eth的api获取对手交易的gasPrice，对手gasUsed，计算对手折算

3.根据1,2的条件满足情况向df_out添加一行

