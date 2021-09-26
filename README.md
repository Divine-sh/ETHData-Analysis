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

output.csv： 输出文件 

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

​		③是否为N+2 或 N+1

​	以上条件都成立时，

​	① 通过**web3.eth.get_transaction_by_block(blockNumber,Index)**得到可能存在的对手的交易hash

​	② 通过logs获得token1和token2

2.判断是否为抢交易：

​	如果是抢交易，

​	① 通过eth的api获取对手交易的gasPrice，对手gasUsed，获得op_timeStamp(和block的timeStamp一致，因为是同一时间打包)

​	② 通过对手交易的hash，用selenium爬取op_toMiner

​	③ 计算对手折算 	

3.根据1,2的条件满足情况向df_out添加一行

## 附加任务：

#### 分析任务-评估 Dex Swap 前十套利者收益情况

### 背景：

##### 1.我们想评估一下，纯DEX的 Swap 套利的利润空间

##### 2.衡量的方式：

##### 	最近1周，通过 Swap套利，给旷工钱最多的10个合约的每日收益

### 逻辑流程

##### 1.最近一周的所有走 FB的交易  

1. [txHash]
2. [423494_2021_09_22.csv](https://r09na2abps.larksuite.com/file/boxusqyiVAfuOM1d5Trt2gU2Y1d) 



##### 2.判断一笔交易是否 Swap套利

1. 获取交易的日志，进行解析

2. 成立条件：

   1. 有至少两笔ERC20 的转账
   2. 且第一笔ERC20 和 最后一笔 ERC20 转账 均为 WETH操作

   

##### 3.实现方法

1. 通过 w3 获取 trx logs
   1. https://cn.etherscan.com/tx/0xd4aea8dfce56d9f4946ac3b8201cc24819b8163619428a6d36df25e2548e4fac#eventlog
   2. 判断是否为 WETH
      1. address 为 '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
   3. 判断是否为 Transfer 转账事件
      1. topics[0] 为 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef



##### 4.能够计算每笔交易给矿工的利润

1. [innerTokens]
   1. Profit = innerToken[-1].balance - inerToken[0].balance
   2. Cost = gasFee + transferToMine
      1. gasFee = gasUsed * gasPrice (链上数据)
      2. transferToMIner = coinbase_transfer（csv中有对应数据）
   3. NetProfit = Profit-Cost



##### 5.按照利润排序，取总利润10



##### 6.最后输出表格

1. contractAddr, dtStr, trxCnt, ProfitSum, netProfitSum
