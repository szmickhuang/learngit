import baostock as bs
import pandas as pd
import csv

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

##### 从csv文件中读取标的列表stocklist，并处理成“sz.xxxxxx”格式

stocklist = list()
with open('/data/jupyter/root/TARGET_INDEX_STOCK_LIST_UTF8.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #temp = (row['品种代码'], row['品种名称'])
        stocklist.append((('sz.' + row['品种代码']), row['品种名称']))

all_result_profit = pd.DataFrame()
for tempid in stocklist:
    profit_list = []
    rs_profit = bs.query_profit_data(code=tempid[0], year=2019, quarter=4)
    while (rs_profit.error_code == '0') & rs_profit.next():
        profit_list.append(rs_profit.get_row_data())
    result_profit=pd.DataFrame(profit_list, columns=rs_profit.fields)
    all_result_profit = all_result_profit.append(result_profit, ignore_index=True)