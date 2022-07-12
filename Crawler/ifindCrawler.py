from iFinDPy import *
import pandas as pd
import numpy as np

class judge_good_or_bad_swindex():

    def __init__(self,interval,percentage,act,psw):
        self.interval = interval
        self.percentage = percentage
        self.act = act
        self.psw = psw

    def thslogin(self):
        # 输入用户的帐号和密码
        thsLogin = THS_iFinDLogin(self.act,self.psw)
        print(thsLogin)
        if thsLogin != 0:
            print('登录失败')
        else:
            print('登录成功')

    def history_swindex(self):
        # 通过历史行情板块提取申万一级行业指数
        data_swindex = THS_HQ('801010.SL,801030.SL,801040.SL,801050.SL,801080.SL,801110.SL,'
                              '801120.SL,801130.SL,801140.SL,801150.SL,801160.SL,801170.SL,'
                              '801180.SL,801200.SL,801210.SL,801230.SL,801710.SL,801720.SL,'
                              '801730.SL,801740.SL,801750.SL,801760.SL,801770.SL,801780.SL,'
                              '801790.SL,801880.SL,801890.SL,801950.SL,801960.SL,801970.SL,801980.SL',
                              'close', '', '2019-07-12', '2022-07-12')

        if data_swindex.errorcode != 0:
            print('error:{}'.format(data_swindex.errmsg))
        else:
            data_result = data_swindex
            return data_result.data

    def judgegoodorbad(self,data,interval,percentage):
        good_or_bad = []
        data = data.reset_index(drop=True)
        for i in data.index:
            value = data.iloc[i:i+interval,:]
            if len(value) < interval:
                value = data.iloc[i:,:]
                # print(value)
                x = value.copy()
                index = x.index
                base = index[0]
                x['percentage'] = (x['close'] - x['close'].loc[base])/x['close'].loc[base]
                if sum(x['percentage'] < percentage) != 0 :
                    result = 'bad'
                else:
                    result = 'good'
                good_or_bad.append(result)
                break
            else:
                # print(value)
                x = value.copy()
                index = x.index
                base = index[0]
                x['percentage'] = (x['close'] - x['close'].loc[base])/x['close'].loc[base]
                if sum(x['percentage'] < percentage) != 0 :
                    result = 'bad'
                else:
                    result = 'good'
                good_or_bad.append(result)
        data = data.iloc[:len(good_or_bad),:]
        y = data.copy()
        y['judge'] = good_or_bad
        return y

    def get_result_df(self):
        data = self.history_swindex()
        code_list = data['thscode'].value_counts().index
        result_df = pd.DataFrame()
        for i in code_list:
            data_to_process = data[data['thscode'] == i]
            result = self.judgegoodorbad(data=data_to_process, interval=self.interval, percentage=self.percentage)
            result_df = pd.concat([result_df, result], ignore_index=True)
        return result_df

if __name__ == '__main__':
    act,psw = "zjdx157", "789202"
    judge = judge_good_or_bad_swindex(interval=20,percentage=-.01,act=act,psw=psw)
    judge.thslogin()
    result = judge.get_result_df()
    print(result)