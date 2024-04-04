import os
import requests

import pandas as pd
import zipfile


def download_raw_dataset(url: str, zip_save_path: str) -> None:
    try:
        response = requests.get(url)

        # Check if the request was successful or not (status code 200)
        if response.status_code != 200:
            print(f"Failed to download file. Status code: {response.status_code}")

        else:
            print(f'Download dataset from "{url}" now...')

            # save to zip
            with open(zip_save_path, 'wb') as file:
                file.write(response.content)
                print(f'Save downloaded file to disk, path=="{zip_save_path}"...')

            # unzip files then save csv files
            if os.path.exists(zip_save_path):
                csv_save_path = ".".join(zip_save_path.split('.')[:-1]) + '.csv'
                with zipfile.ZipFile(zip_save_path) as file:
                    file.extractall(os.path.dirname(zip_save_path))

                print(f'Extract downloaded zip file to csv, path=="{csv_save_path}"...')

            # remove original zip file
            os.remove(zip_save_path)

            # fix some file issue
            tmp_folder_abspath = os.path.abspath(".".join(csv_save_path.split('.')[:-1]))
            print("tmp_folder_abspath: ", tmp_folder_abspath)

            # if os.path.exists(tmp_folder_abspath)\
            #     and os.path.isdir(tmp_folder_abspath):
            #     print("tmp_folder_abspath: ", tmp_folder_abspath)
            #     os.system(f"mv {tmp_folder_abspath}/* {csv_save_path}; rm -rf {tmp_folder_abspath}")
            
    except Exception as e:
        print("Error:", e)


if __name__ == '__main__':
    RAW_DATASET_DIRNAME = "raw_dataset_Youbike2.0票證資料"
    RAW_DATASET_DOWNLOAD_LIST = "raw_dataset_Youbike2.0票證資料_list.csv"
    os.system(f"mkdir -p ./{RAW_DATASET_DIRNAME}")
    df = pd.read_csv(RAW_DATASET_DOWNLOAD_LIST)

    for i in range(df.shape[0]):
        dataset_download_url = df.loc[i, "fileURL"]
        print(f'Try to download file from "{dataset_download_url}" now...')
        
        save_file_path = os.path.join(
            RAW_DATASET_DIRNAME, "".join(dataset_download_url.split('/')[-1]))
        
        download_raw_dataset(dataset_download_url, save_file_path)
        print(" ")

    print("All datasets are downloaded completed!")
    