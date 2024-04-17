# raw dataset link: https://codis.cwa.gov.tw/StationData
# also refer: https://codis.cwa.gov.tw/pdf_data/Readme.pdf?1713346902747

import os
import pandas as pd


def preprocessed_dataset_taipei_weather(df_file_path: str) -> "pandas.core.frame.DataFrame":
    df = pd.read_csv(df_file_path)
    
    # drop the first row
    df = df.iloc[1:, :]

    # create index
    date = df_file_path.split('/')[-1].split('.')[0].replace("466920-", "")
    df["time"] = df["觀測時間(hour)"].apply(lambda x: f"{date} {int(x)-1}:00:00")
    df["time"] = pd.to_datetime(df["time"]) + pd.Timedelta(hours=1)

    return df.drop(columns=["觀測時間(hour)"]).set_index("time")


if __name__ == '__main__':
    RAW_DATASET_ROOT = "raw_dataset_臺北(466920)測站時序圖日報表(逐時資料)"
    df = pd.DataFrame()

    for folder_name in sorted(os.listdir(RAW_DATASET_ROOT)):
        folder_abspath = os.path.join(os.path.abspath(RAW_DATASET_ROOT), folder_name)

        if not os.path.isdir(folder_abspath):
            continue

        for file_name in sorted(os.listdir(folder_abspath)):
            file_abspath = os.path.join(folder_abspath, file_name)
            _df = preprocessed_dataset_taipei_weather(file_abspath)

            assert _df.shape[0] == 24, f"please re-download the file {file_name}"
            df = pd.concat([df, _df])
            print(f"file {file_name} has been converted, current dataframe shape is {df.shape}")


    save_abspath = os.path.join(
        os.path.dirname(__file__), "preprocessed_dataset_臺北(466920)測站時序圖日報表(逐時資料).csv")
    df.to_csv(save_abspath)
    print(f"dataframe has been save to disk! file abspath=={save_abspath}")
