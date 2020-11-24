# 获得基金列表
df = get_all_securities(['fund'])
# 获得etf基金列表
etfs = df[df['type']=='etf']
# 获得分级A基金列表
#fjas = df[df['type']=='fja']
# 获得分级B基金列表
#fjbs = df[df['type']=='fjb']

# 获得所有股票列表
#stocks = get_all_securities(['stock'])

# 选取15年以前上市的基金和股票
jijinE = []
#jijinA = []
#jijinB = []
#gupiao = []
for i in range(len(etfs.start_date)):
    if etfs.start_date[i].year < 2015:
        jijinE.append(etfs.index[i])
#for i in range(len(fjas.start_date)):
#    if fjas.start_date[i].year < 2015:
#        jijinA.append(fjas.index[i])
#for i in range(len(fjbs.start_date)):
#    if fjbs.start_date[i].year < 2015:
#        jijinB.append(fjbs.index[i])
#for i in range(len(stocks.start_date)):
#    if stocks.start_date[i].year < 2015:
#        gupiao.append(stocks.index[i])