# from WindPy import w
import pandas as pd


# w.start()
# w.isconnected()


class judge_stock_disaster(object):
    def __init__(self,data):
        self.data=data
    # def data_process(self):
    #     # 导入原始数据
    #     raw_data = pd.DataFrame()
    #     for code in self.codes:
    #         error_code, data = w.wsd(code, "close", self.start_date, self.end_date, "", usedf=True)
    #         # print(data)
    #         raw_data = pd.concat([raw_data, data], axis=1)
    #     raw_data.columns = self.codes
    #     return raw_data

    # 读取本地数据
    def data_load(self):
        new_data=self.data
        new_data.index = new_data.iloc[:, 0]
        new_data = new_data.drop(index=new_data.index[0], columns=new_data.columns[0])
        return new_data

    # 判断是否股灾，方法为遍历每一天的收盘价，和之后20个每一个交易日的收盘价进行涨跌幅的计算，若有一天涨跌幅低于阈值即判断为股灾
    def judge_disaster(self, col_data, interval, percentage):
        raw_data = self.data_load()
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
        raw_data = self.data_load()
        result = pd.DataFrame()
        for col in raw_data.columns:
            col_data = raw_data[col]
            tmp = self.judge_disaster(col_data, interval, percentage)
            result = pd.concat([result, tmp], axis=1)
        result.columns = raw_data.columns
        return result


if __name__ == '__main__':
    raw_data = pd.read_excel('指数.xlsx')
    x = judge_stock_disaster(raw_data)
    #interval表示后多少交易日，percentage表示涨跌幅阈值
    result = x.main(interval=20, percentage=-0.2)
    # print(result)
    result.to_excel('result.xlsx', engine='openpyxl')
