import os
import pandas as pd


if __name__ == '__main__':
    PROCESSED_DATASET_1_DIRNAME = "preprocessed_dataset_Youbike2.0票證資料_1"
    # df = pd.DataFrame()

    # # merge to a big dataframe
    # for filename in [f for f in os.listdir(PROCESSED_DATASET_1_DIRNAME) 
    #                  if f.endswith('.csv')]:
    #     file_abspath = os.path.join(os.path.abspath(PROCESSED_DATASET_1_DIRNAME), filename)
    #     df = pd.concat([df, pd.read_csv(file_abspath, encoding="utf-8-sig")], axis=0)
    #     print(df.shape)

    # # sort, reset_index, then save
    # print("sort")
    # df = df.sort_values(["rent_time", "return_time"])
    # print("reset_index")
    # df = df.reset_index(drop=True)
    # print(df)
    # print("save")
    # # df.to_csv("preprocessed_dataset_Youbike2.0票證資料_2.csv", 
    # #           encoding="utf-8-sig", compression='gzip')
    # df.to_csv("preprocessed_dataset_Youbike2.0票證資料_2.csv", 
    #           encoding="utf-8-sig", index=False)
    # del df
    # print("merge completed!")

    # check and try to read dataframe again
    # df = pd.read_csv("preprocessed_dataset_Youbike2.0票證資料_2.csv", encoding="utf-8-sig")
    # df = pd.read_csv("preprocessed_dataset_Youbike2.0票證資料_2.csv")
    df = pd.read_csv("preprocessed_dataset_Youbike2.0票證資料_2_zip.csv")
    # df.to_csv("preprocessed_dataset_Youbike2.0票證資料_2_zip.csv", 
    #           encoding="utf-8-sig", index=False, compression='gzip')
    print(df)
