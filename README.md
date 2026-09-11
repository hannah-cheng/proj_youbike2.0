# 臺大周邊 YouBike 2.0 資料整理

本專案蒐集並整理臺大校園周邊的 YouBike 2.0 資料，內容涵蓋歷史票證旅次、臺北測站逐時氣象，以及臺大周邊站點的即時車輛資訊。這些資料可作為後續交通流量、租借行為與天氣關聯分析的基礎。

## 資料處理流程

1. 依下載清單取得每月 YouBike 2.0 票證資料。
2. 保留借車站或還車站名稱包含「臺大」的旅次。
3. 將各月份的篩選結果合併為單一資料集。
4. 將中央氣象署臺北測站的每日資料整理成逐時時間序列。
5. 定時擷取臺大周邊 YouBike 站點的即時可借、可還車位資訊。

## 專案內容

| 檔案或目錄 | 說明 |
| --- | --- |
| `raw_dataset_Youbike2.0票證資料_list.csv` | 每月票證資料的下載網址清單。 |
| `raw_dataset_Youbike2.0票證資料_downloader.py` | 依清單下載並解壓縮原始票證資料。 |
| `raw_dataset_Youbike2.0票證資料/` | 原始月資料存放目錄；大型資料檔不納入 Git。 |
| `preprocessed_dataset_Youbike2.0票證資料_1.py` | 篩選與臺大相關的旅次，並保留借還時間、站點及騎乘時間。 |
| `preprocessed_dataset_Youbike2.0票證資料_1/` | 各月份的票證篩選結果；大型資料檔不納入 Git。 |
| `preprocessed_dataset_Youbike2.0票證資料_2.py` | 合併月資料的實驗腳本。 |
| `preprocessed_dataset_臺北(466920)測站時序圖日報表(逐時資料)_1.py` | 將臺北測站每日 24 筆觀測資料合併為逐時時間序列。 |
| `preprocessed_dataset_臺北(466920)測站時序圖日報表(逐時資料).csv` | 整理後的臺北測站逐時氣象資料。 |
| `get_realtime_data.py` | 持續擷取臺大周邊站點的 YouBike 即時資訊。 |
| `YouBike2.0臺北市公共自行車即時資訊/` | 即時資訊擷取結果。 |

## 主要資料欄位

### 票證旅次資料

- `rent_time`：借車時間。
- `rent_station`：借車站點。
- `return_time`：還車時間。
- `return_station`：還車站點。
- `rent`：騎乘時間。

### 氣象資料

以 `time` 為時間索引，包含氣壓、氣溫、露點、相對溼度、風速、風向、降水量、日照、能見度、紫外線指數與雲量等欄位。

### 即時站點資料

包含站點名稱與編號、行政區、地址、資料更新時間、總車位數、可借車輛數、可還車位數及經緯度等欄位。

## 執行環境

建議使用 Python 3.9 以上版本。專案目前沒有套件鎖定檔，主要相依套件為：

- `pandas`
- `requests`

可在專案根目錄建立環境並安裝：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pandas requests
```

## 使用方式

以下指令皆應在專案根目錄執行。

下載票證原始資料：

```bash
python raw_dataset_Youbike2.0票證資料_downloader.py
```

篩選臺大相關旅次：

```bash
python preprocessed_dataset_Youbike2.0票證資料_1.py
```

整理臺北測站逐時資料：

```bash
python 'preprocessed_dataset_臺北(466920)測站時序圖日報表(逐時資料)_1.py'
```

開始蒐集即時站點資料：

```bash
python get_realtime_data.py
```

即時蒐集程式會持續執行，可使用 `Ctrl+C` 結束。

## 資料來源

- [臺北市 YouBike 2.0 即時資訊](https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json)
- [中央氣象署 CODiS 測站資料](https://codis.cwa.gov.tw/StationData)
- YouBike 2.0 歷史票證資料網址收錄於 `raw_dataset_Youbike2.0票證資料_list.csv`。

## 注意事項

- 原始資料與部分前處理結果檔案很大，相關資料目錄已由 `.gitignore` 排除；重新複製專案後，需自行下載或準備資料。
- `preprocessed_dataset_Youbike2.0票證資料_1.py` 目前設定只處理排序後索引第 39 筆起的月資料。若要完整重建，請先調整程式中的 `if i >= 39` 條件。
- `preprocessed_dataset_Youbike2.0票證資料_2.py` 的合併程式碼目前被註解，直接執行時會改為讀取 `preprocessed_dataset_Youbike2.0票證資料_2_zip.csv`；使用前需依需求調整。
- 即時資料輸出雖使用 `.csv` 副檔名，實際內容採 gzip 壓縮；以 pandas 讀取時需指定 `compression="gzip"`。
- 資料使用與再散布前，請確認各來源的最新授權條款與使用規範。
