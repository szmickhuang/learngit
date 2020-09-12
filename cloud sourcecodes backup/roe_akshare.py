import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt

#TARGET_ETF = 'sh510500' # 中证500ETF
TARGET_ETF = 'sz159949' # 华安创业板50ETF
TARGET_INDEX = '399673' # 创业板50指数
#TARGET_ETF = 'sh510300' # 沪深300ETF
#TARGET_ETF = 'sh501050' # 50AHETF LOF
#TARGET_ETF = 'sh512100' # 中证1000ETF

REGULAR_INPUT = 200.0     # 常规定投金额
ADD_INPUT= 500          #加投金额
ADD_TIMES = 3.0           # 追加倍数
ADD_INPUT_LIMIT = -0.03   # 即下跌4%触发加投

def addinput(x):
    if (x < ADD_INPUT_LIMIT):
        return ADD_INPUT
    else:
        return 0
    
def print_etf_backtest(hist_df):
    total_share = hist_df['share'].sum()
    total_value = total_share * fund_etf_hist_df.iloc[-1,2]
    total_fix_invest = fund_etf_hist_df['Fixed_Input'].sum()
    total_additional_invest = fund_etf_hist_df['Additional'].sum()
    total_benefits = total_value - total_fix_invest - total_additional_invest
    
    print('定投总金额: %.2f' %total_fix_invest)
    print('额外总金额：%.2f' %total_additional_invest)
    print('获得总份数：%.2f' %total_share)
    print('市值总金额: %.2f' %total_value)
    print('投资总收益: %.2f' %total_benefits)
    print('投资收益率: {:.2%}' .format(total_benefits/(total_fix_invest+total_additional_invest)))
    
    return

def dealwith_etf_hist():
    fund_etf_hist_df = ak.fund_etf_hist_sina(symbol=TARGET_ETF)
    
    # 把当日最高价、最低价两列数据drop掉
    fund_etf_hist_df = fund_etf_hist_df.drop(['high', 'low', 'volume'], axis=1)
    # 增加‘常规定投’数据列
    fund_etf_hist_df['Fixed_Input'] = REGULAR_INPUT
    # 处理常规定投得到的份额
    # 增加‘日增长率’数据列
    fund_etf_hist_df['Daily_Increase'] = (fund_etf_hist_df['close'] - fund_etf_hist_df['close'].shift(1)) / fund_etf_hist_df['close'].shift(1)
    fund_etf_hist_df.iloc[0,4] = 0 # 第一行的处理为0
    
    fund_etf_hist_df['Additional'] = fund_etf_hist_df['Daily_Increase'].map(addinput)
    
    fund_etf_hist_df['share'] = (fund_etf_hist_df['Fixed_Input']+fund_etf_hist_df['Additional'])/fund_etf_hist_df['close'].shift(-1)
    
    fund_etf_hist_df.iloc[-1, 6] = 0 # 最后一天份数设为0
    fund_etf_hist_df.iloc[-1, 3] = 0 # 最后一天定投金额设为0
    
    return fund_etf_hist_df

index_stock_cons_df = ak.index_stock_cons(index=TARGET_INDEX)
index_stock_cons_df.to_csv('/data/jupyter/root/TARGET_INDEX_STOCK_LIST_GBK.csv', encoding = "gbk")
index_stock_cons_df.to_csv('/data/jupyter/root/TARGET_INDEX_STOCK_LIST_UTF8.csv')

temp1 = ak.stock_financial_abstract(stock=300782).head(5)
temp1['股票编码'] = 300782
temp2 = ak.stock_financial_abstract(stock=300661).head(5)
temp2['股票编码'] = 300661

temp1 = temp1.append(temp2).reindex()
temp1

temp1.append(temp2).to_csv('/data//jupyter/root/temp.csv')

stock_financial_abstract_df = pd.DataFrame()
for loop_index in index_stock_cons_df['品种代码']:
    stock_financial_abstract_df = stock_financial_abstract_df.append(ak.stock_financial_abstract(stock=loop_index).head(2))