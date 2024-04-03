import os

import pandas as pd
import requests


def download_file(url: str, save_path: str) -> None:
    try:
        response = requests.get(url)

        # Check if the request was successful or not (status code 200)
        if response.status_code != 200:
            print(f"Failed to download file. Status code: {response.status_code}")

        else:
            print(f'Download dataset from "{url}" now...')

            with open(save_path, 'wb') as file:
                file.write(response.content)
                print(f'Save downloaded file to disk, path=="{save_path}"...')
            
    except Exception as e:
        print("Error:", e)


if __name__ == '__main__':
    DATASET_DIRNAME = "dataset_zip"
    DATASET_DOWNLOAD_LIST = "dataset_zip_list.csv"
    os.system(f"mkdir -p ./{DATASET_DIRNAME}")
    df = pd.read_csv(DATASET_DOWNLOAD_LIST)

    for i in range(df.shape[0]):
        dataset_download_url = df.loc[i, "fileURL"]
        print(f'Try to download file from "{dataset_download_url}" now...')
        
        save_file_path = os.path.join(
            DATASET_DIRNAME, "".join(dataset_download_url.split('/')[-1]))
        download_file(dataset_download_url, save_file_path)
        print(" ")

    print("All datasets are downloaded completed!")
    