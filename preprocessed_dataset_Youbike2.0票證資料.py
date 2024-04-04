import json
import os
import requests

import pandas as pd


def _get_ntu_station_list() -> list:
    '''get all youbike 2.0 station names if the station inside NTU campus
    input args: None
    output args: list of str, content has been mentioned above
    '''

    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    r = requests.get(url)
    station_list = json.loads(r.text)
    ret = []

    for station in station_list:
        if ("臺大" in station["sna"]) or ("台大" in station["sna"]):
            ret.append(station["sna"])

    return ret


def preprocess_raw_dataset(csv_file_path: str) -> "pandas.core.frame.DataFrame":
    '''filter all raw data, then remain all youbike rent/return records inside NTU;
    otherwise if neither rent nor return station not in NTU campus, ignore them

    input args: 
        - src_path: str, path of the zip dataset downloaded from the website

    output args: None
    '''

    df = pd.read_csv(csv_file_path) 
    df = pd.DataFrame({
        # "infodate": df.iloc[:, 5],
        "rent_time": df.iloc[:, 0],
        "rent_station": df.iloc[:, 1],
        "return_time": df.iloc[:, 2],
        "return_station": df.iloc[:, 3],
        "rent": df.iloc[:, 4]
    })
    df = df.sort_values(["rent_time", "return_time"]).reset_index(drop=True)
    filter_set = _get_ntu_station_list()
    filtered_df = df[df['rent_station'].isin(filter_set) | df['return_station'].isin(filter_set)].reset_index(drop=True)
    print(filtered_df)
    return filtered_df


if __name__ == '__main__':
    RAW_DATASET_DIRNAME = "raw_dataset_Youbike2.0票證資料"
    # PREPROCESSED_DATASET_DIRNAME = "preprocessed_dataset_Youbike2.0票證資料"
    file_abspath_list = [os.path.abspath(file_name) for file_name in os.listdir(RAW_DATASET_DIRNAME)]
    # file_abspath_list = ["/Users/hannah_cheng/Scripts/proj_youbike2.0/raw_dataset_Youbike2.0票證資料/202311_YouBike2.0▓╝├╥¿ΩÑd╕Ω«╞.csv"]

    for file_abspath in file_abspath_list:
        print(f'Preprocessing file "{file_abspath_list}" now...')
        df = preprocess_raw_dataset(file_abspath)
        print(df)
        break
    