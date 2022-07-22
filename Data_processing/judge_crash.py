import numpy as np
import pandas as pd


class judge_stock_disaster(object):
    def __init__(self,data):
        self.data=data

    # 判断是否股灾，方法为遍历每一天的收盘价，和之后20个每一个交易日的收盘价进行涨跌幅的计算，若有一天涨跌幅低于阈值即判断为股灾
    def judge_disaster(self, col_data, interval, percentage):
        raw_data = self.data
        IsDisaster = []
        for i in range(len(col_data)):
            value = col_data[i:i + interval]
            base = value[0]
            if base == 0:
                pass
            else:
                for compare in value:
                    if (compare - base) / base < percentage:
                        IsDisaster.append(raw_data.index[i])
                        break
        return pd.Series(IsDisaster)

    #核心函数,遍历每一个指数
    def main(self, interval, percentage):
        raw_data = self.data
        result = pd.DataFrame()
        for col in raw_data.columns:
            col_data = raw_data[col]
            tmp = self.judge_disaster(col_data, interval, percentage)
            result = pd.concat([result, tmp], axis=1)
        result.columns = raw_data.columns
        result = result.values.ravel()
        result = np.unique(result)
        result = pd.DataFrame({'股灾时间点':result})
        return result


if __name__ == '__main__':
    raw_data = pd.read_excel(r'指数.xlsx',index_col=0,header=0,skiprows=1)
    x = judge_stock_disaster(raw_data)
    #interval表示后多少交易日，percentage表示涨跌幅阈值
    result = x.main(interval=20, percentage=-0.2)
    result.to_csv(r'./result.csv')