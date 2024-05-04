import datetime
import os
import pandas as pd
import requests
import time


def get_youbike_realtime_data() -> "pandas.core.frame.DataFrame":
    url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
    resp = requests.get(url=url)
    _df = pd.json_normalize(resp.json())
    _df = _df[~_df['sna'].str.contains("臺大醫學院|臺大醫院") & _df['sna'].str.contains("臺大", na=False)]
    _df["sna"] = _df["sna"].apply(lambda x: x.split('_')[1])
    _df["time"] = _df["srcUpdateTime"].apply(lambda x: f"{x[:-3]}:00")
    return _df.set_index(["sna", "time"]).sort_index()


def create_empty_dataframe() -> tuple:
    _df = pd.DataFrame()
    _df_abspath = f"{os.getcwd()}/YouBike2.0臺北市公共自行車即時資訊/YouBike2.0臺北市公共自行車即時資訊(raw_dataset)_{datetime.datetime.now()}.csv"
    print(_df_abspath)
    return (_df, _df_abspath)


if __name__ == "__main__":
    (df, df_abspath) = create_empty_dataframe()

    while True:    
        if datetime.datetime.now().second == 0:
            try:
                _df = get_youbike_realtime_data()
            except:
                time.sleep(1)
                (df, df_abspath) = create_empty_dataframe()
                _df = get_youbike_realtime_data()
            
            df = pd.concat([df, _df], axis=0)
            df.to_csv(df_abspath, compression="gzip", encoding='utf-8-sig')
            print(df.tail(5))
            print(datetime.datetime.now(), df.shape)
        else:
            time.sleep(1)
