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

    # try:
        # print('entry')
    df = pd.read_csv(csv_file_path)
    # df = pd.read_csv(csv_file_path, encoding="latin-1")
    # df = pd.read_csv(csv_file_path, encoding="utf-8-sig")
    # df = pd.read_csv(csv_file_path, encoding="gb18030")
    # df = pd.read_csv(csv_file_path, encoding="cp1252")
        # df = pd.read_csv(csv_file_path, encoding="utf-8")
        # df = pd.read_csv(csv_file_path, 
        #                  usecols=['rent_time', 'rent_station', 'return_time', 'return_station', 'rent'], 
        #                  encoding="utf-8")
        # # print("except!")
        # df.to_csv(csv_file_path, encoding='utf-8-sig')
        # df.to_csv(csv_file_path, encoding='utf-8')
    # except UnicodeDecodeError:
    #     print("except!")
        # pass
    #     # df = pd.read_csv(csv_file_path, encoding="utf-8")
    #     # df = pd.read_csv(csv_file_path, encoding="ISO-8859-1")  # utf-8
    #     # df = pd.read_csv(csv_file_path, encoding="utf-8-sig")
    #     # df = pd.read_csv(csv_file_path, encoding="gbk")
    #     # df = pd.read_csv(csv_file_path, encoding="gb18030")
    #     # df = pd.read_csv(csv_file_path, encoding="cp1252")
    #     df = pd.read_csv(csv_file_path, encoding="latin-1")
    #     # df = pd.read_csv(csv_file_path, encoding="utf-8-sig")
    #     df.to_csv(csv_file_path, encoding='utf-8-sig')
    #     del df
    #     df = pd.read_csv(csv_file_path, encoding="utf-8-sig")
    #     # encoding_list = ['ascii', 'big5', 'big5hkscs', 'cp037', 'cp273', 'cp424', 'cp437', 'cp500', 'cp720', 'cp737', 
    #     #                  'cp775', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp858', 'cp860', 'cp861', 'cp862', 
    #     #                  'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 
    #     #                  'cp1006', 'cp1026', 'cp1125', 'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 
    #     #                  'cp1255', 'cp1256', 'cp1257', 'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 
    #     #                  'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 
    #     #                  'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2', 
    #     #                  'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 
    #     #                  'iso8859_10', 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'iso8859_16', 'johab', 
    #     #                  'koi8_r', 'koi8_t', 'koi8_u', 'kz1048', 'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2', 
    #     #                  'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_32', 
    #     #                  'utf_32_be', 'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8', 'utf_8_sig']

        # # for encoding in encoding_list:
        # for i in range(len(encoding_list)):
        #     print(i)
        #     print(encoding_list[i])
        #     encoding = encoding_list[i]

        #     if i < 100:
        #         continue

        #     # worked = True
        #     try:
        #         # df = pd.read_csv(csv_file_path, encoding=encoding, nrows=5)
        #         df = pd.read_csv(csv_file_path, encoding=encoding)
        #         break
        #     except:
        #         # worked = False
        #         pass

        #     # if worked:
        #     #     print(encoding, ':\n', df.head())

        #     if df.shape[0]:
        #         print(encoding)
        #         break
    
    df = pd.DataFrame({
        # "infodate": df.iloc[:, 5],
        "rent_time": df.iloc[:, 0],
        "rent_station": df.iloc[:, 1],
        "return_time": df.iloc[:, 2],
        "return_station": df.iloc[:, 3],
        "rent": df.iloc[:, 4]
    })

    print(df)
    # df.to_csv(csv_file_path, index=False)
    # filter_set = _get_ntu_station_list()
    # filtered_df = df[df['rent_station'].isin(filter_set) | df['return_station'].isin(filter_set)].reset_index(drop=True)
    filtered_df = df[df['rent_station'].str.contains("臺大") | df['return_station'].str.contains("臺大")]
    filtered_df = pd.DataFrame({
        # "infodate": df.iloc[:, 5],
        "rent_time": filtered_df.iloc[:, 0],
        "rent_station": filtered_df.iloc[:, 1],
        "return_time": filtered_df.iloc[:, 2],
        "return_station": filtered_df.iloc[:, 3],
        "rent": filtered_df.iloc[:, 4]
    })

    filtered_df = filtered_df.sort_values(["rent_time", "return_time"]).reset_index(drop=True)
    print(filtered_df)
    del df
    
    return filtered_df


if __name__ == '__main__':
    PROJECT_ABSPATH = os.path.abspath(os.path.dirname(__file__))
    RAW_DATASET_DIRNAME = "raw_dataset_Youbike2.0票證資料"
    PREPROCESSED_DATASET_DIRNAME = "preprocessed_dataset_Youbike2.0票證資料_1"
    os.system(f"mkdir -p {PREPROCESSED_DATASET_DIRNAME}")
    li = [f for f in os.listdir(RAW_DATASET_DIRNAME) if f.endswith('.csv')]
    li.sort()
    li = li

    for i in range(len(li)):
        # print('\n\n\n\n\n')
        # file_name = li[i]
        # print(i)
        # print(file_name)

        # src_file_abspath  = os.path.join(
        #     os.path.join(PROJECT_ABSPATH, RAW_DATASET_DIRNAME), 
        #     file_name
        # )
        # dest_file_abspath = os.path.join(
        #     os.path.join(PROJECT_ABSPATH, PREPROCESSED_DATASET_DIRNAME), 
        #     file_name
        # )

        # print(f'Preprocessing file "{src_file_abspath}" now...')
        # df = preprocess_raw_dataset(src_file_abspath)

        # # save csv file
        # # df.to_csv(dest_file_abspath, encoding="latin-1")
        # df.to_csv(dest_file_abspath, encoding="utf-8-sig", index=False)
        
        # if i >= 31:
        if i >= 39:
            print('\n\n\n\n\n')
            file_name = li[i]
            print(i)
            print(file_name)

            src_file_abspath  = os.path.join(
                os.path.join(PROJECT_ABSPATH, RAW_DATASET_DIRNAME), 
                file_name
            )
            dest_file_abspath = os.path.join(
                os.path.join(PROJECT_ABSPATH, PREPROCESSED_DATASET_DIRNAME), 
                file_name
            )
            
            print(f'Preprocessing file "{src_file_abspath}" now...')
            df = preprocess_raw_dataset(src_file_abspath)

            # save csv file
            # df.to_csv(dest_file_abspath, encoding="latin-1", index=False)
            df.to_csv(dest_file_abspath, encoding="utf-8-sig", index=False)
            