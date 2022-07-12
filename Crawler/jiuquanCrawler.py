import requests
from datetime import date,time,datetime
import time
import pandas as pd


def jiucai_crawler(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'}
    params = {"id": 4, "type": "pc", "data_source": "xichou", "version": "2.0.0", "authtoken": "",
              "act_time": 1657524892197, "tirgkjfs": "7a", "abiokytke": "e8", "u54rg5d": "37",
              "kf54ge7": "3", "tiklsktr4": "a", "lksytkjh": "b430", "sbnoywr": "fc", "bgd7h8tyu54": "a8",
              "y654b5fs3tr": "5", "bioduytlw": "9", "bd4uy742": "2", "h67456y": "5b4", "bvytikwqjk": "a8",
              "ngd4uy551": "b4", "bgiuytkw": "4f", "nd354uy4752": "b", "ghtoiutkmlg": "501", "bd24y6421f": "c1",
              "tbvdiuytk": "5", "ibvytiqjek": "2d", "jnhf8u5231": "4f", "fjlkatj": "379", "hy5641d321t": "12",
              "iogojti": "1",
              "ngd4yut78": "01", "nkjhrew": "2", "yt447e13f": "4", "n3bf4uj7y7": "4", "nbf4uj7y432": "e8",
              "yi854tew": "6b",
              "h13ey474": "6b3", "quikgdky": "69"}
    try:
        res = requests.post(url=url, headers=headers, data=params)
        if res.status_code == 200:
            result = res.json()
            result = result['data']['canvas_data']['series'][0]['data']
            col_time = []
            col_data = []
            for i in result:
                time_local = time.localtime(i[0] / 1000)
                dt = time.strftime('%Y-%m-%d', time_local)
                data = i[1]
                col_time.append(dt)
                col_data.append(data)
                df = pd.DataFrame({'日期': col_time, '沪深300股指期货升贴水': col_data})
            return df
    except requests.RequestException:
        return None

if __name__ == '__main__':
    url = r'https://api.jiucaishuo.com/v2/kjtl/getlist'
    result = jiucai_crawler(url=url)
    print(result)