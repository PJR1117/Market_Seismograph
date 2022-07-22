import numpy as np
import pandas as pd
import os
import time


class SecDetect:
    def __init__(self, data,benchmark, type='基金' or '股票',
                 unique=False):

        self.benchmark = benchmark
        self.unique = unique
        self.data = data
        self.sec_name = self.data.iloc[0,0]
        self.data = self.data.iloc[:,[2,3]]
        self.index = [[i, i + 1] for i in range(len(self.data) - 1) if (self.data.iloc[i][1] is not np.nan) & (
                    self.data.iloc[i][1] > self.data.iloc[i + 1][1])] # 生成相邻的起始非空并且份额净值递减索引
        assert type == '基金' or type == '股票' , "type 只能是 '基金'或者'股票' "
        self.type = type

    def merge(self, index):
        '''

        :param index: 值长度为2的值递减索引列表
        :return: 将间隔小于三的索引进行合并的列表,应该是去除休息日的影响
        '''
        if len(index) < 2:
            return index
        if len(index) >= 2:
            left = self.merge(index[:int(len(index) / 2)])
            right = self.merge(index[int(len(index) / 2):])
            if right[0][0] - left[-1][1] < 3:
                right[0] = [left[-1][0], right[0][1]]
                return left[:-1] + right
            else:
                return left + right

    def writeDF(self):
        """

        :return: 形成提取基金代码/起始日期/结束日期/持续日期/下跌幅度的df
        """
        index = self.merge(self.index)

        # index = [i for i in index if
        #               (self.data.iloc[i[1]][1] - self.data.iloc[i[0]][1]) / self.data.iloc[i[0][1]] <= self.benchmark]
        if self.unique == True:
            self.index = [self.index[0]]  # 取第一部分的索引段

        index_2 = []
        for i in index:
            returns = (self.data.iloc[i[1]][1] - self.data.iloc[i[0]][1])
            returns_rat = returns / self.data.iloc[i[0]][1]
            if returns_rat <= self.benchmark:
                index_2.append(i)

        if self.type == '基金' :
            DF = [{'基金代码': self.sec_name,
                   '基金净值大幅下跌起始日期': self.data.iloc[i[0]]['日期'], '基金净值大幅下跌结束日期': self.data.iloc[i[1]]['日期'],
                   '基金净值下跌持续的交易日': i[1] - i[0] ,
                   '基金净值下跌的幅度': (self.data.iloc[i[1]]['单位净值(元)'] - self.data.iloc[i[0]]['单位净值(元)']) / self.data.iloc[i[0]]['单位净值(元)']}
                  for i in index_2]
        else:
            DF = [{'公司代码': self.sec_name,
                   '公司股价大幅下跌起始日期': self.data.iloc[i[0]]['日期'], '公司股价大幅下跌结束日期': self.data.iloc[i[1]]['日期'],
                   '公司股价下跌持续的交易日': i[1] - i[0] ,
                   '公司股价下跌的幅度': (self.data.iloc[i[1]]['市盈率'] - self.data.iloc[i[0]]['市盈率']) / self.data.iloc[i[0]]['市盈率']}
                  for i in index_2]
        return pd.DataFrame(DF)

def gen_file(dirname,benchmark,_type='基金' or '股票'):
    assert _type == '基金' or _type == '股票'
    result = pd.DataFrame()
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            data = pd.read_csv(apath,encoding='gbk').iloc[:,0:4]
            selected = SecDetect(data=data,benchmark=benchmark,type=_type).writeDF()
            result = pd.concat([result,selected])
    return result

if __name__ == '__main__':
    dirname = r'D:\data\python\risk_cockpit\data\stock'
    result = gen_file(dirname=dirname,benchmark=-0.2,_type='股票').reset_index(drop=True)
    result.to_csv(r'./股票暴跌.csv',encoding='gbk')