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

### 一、分析任务：评估 Dex Swap 前十套利者收益情况

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
   
   ```python
   trx_rep = w3.eth.get_transaction_receipt(tx)
   trx_log = trx_rep.logs
   {
       'blockHash': HexBytes('0xdb749ad864d5e2e842d44b846e73f047ef93fa7e18a399682a50213be06c1b59'), 
       'blockNumber': 13230393, 
       'contractAddress': None, 
       'cumulativeGasUsed': 854679, 
       'effectiveGasPrice': 34301104282, 
       'from': '0x98313Ec873eA0Ca63623C1EaBB4EdD2129F73EF2', 
       'gasUsed': 174865, 
       'logs': [], 
       'logsBloom': , 
       'status': 1, 
       'to': '0xE592427A0AEce92De3Edee1F18E0157C05861564', 
       'transactionHash': HexBytes('0x000035d6403e5e32384a79708f5ab59a370a00061ab4606e6cb599439d2d45e7'), 
       'transactionIndex': 6, 
       'type': '0x2'
   }
   ```
   
   
   
   1. 判断是否为 WETH
      1. address 为 '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
   2. 判断是否为 Transfer 转账事件
      1. topics[0] 为 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef



##### 4.能够计算每笔交易给矿工的利润

1. [innerTokens]
   1. Profit = innerToken[-1].balance - innerToken[0].balance（开始和最后WETH的价差）
   2. Cost = gasFee + transferToMine
      1. gasFee = gasUsed * gasPrice (链上数据)
      2. transferToMIner = coinbase_transfer（csv中有对应数据）
   3. NetProfit = Profit-Cost



##### 5.按照利润排序，取总利润10

​	按照合约地址group by得到trxCnt, ProfitSum，netProfitSum，然后按照netProfitSum排序



##### 6.最后输出表格

1. contractAddr, dtStr, trxCnt, ProfitSum, netProfitSum

   contractAddr-->csv 中的 toAddr

   dtStr-->csv 中的 Timestamp 格式年月日

   trxCnt：统一toAddress对应交易数量

2. 把所有的套利交易输出到一个单独表arbitrageTrx



### 二、分析任务：Flashbot-GasPrice-调研



## 目的：

调研fb包含的交易是否为当前block 等效gasprice最高的交易。

是否存在一些高优账户的等效gasprice不是最高，但也包含进入fb交易的。



## 手段：

调研fb交易最低gas price，在对应block里非fb交易中gas price分位数。

##### 举例

某block，0-5 的6笔交易为fb交易，6-200的交易为非fb交易。

计算position5的等效gas price 在position 6-200的gas price的分位数。



# 开发资源



## Flashbot API

https://blocks.flashbots.net/v1/blocks?block_number=13383860

curl --location --request GET 'https://blocks.flashbots.net/v1/blocks?block_number=13383860'



## MySQL

### db

mysql -h rm-2zetcrfz7vg3ay7do125030pm.mysql.rds.aliyuncs.com -u r_fb_buddels_users  -D fb_buddles -p

密码：EqgJoRLguk2CKrMZ



### query-包含 fb 的 block

```
select * from block_info limit 50
```



# Web3 访问

使用dataframe的describe求分位数、分位点
