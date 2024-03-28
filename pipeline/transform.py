from os import listdir, path, remove
import pandas as pd

def combine_files_into_dataframe(filename: str, folder: str) -> bool:
    csv_files = [file for file in listdir(folder) if file.endswith(".csv")]
    upload_csv_file = f"{folder}/{filename}.csv"

    for file in csv_files:
        number_id = (file.split("T3_T"))[1].split("_")[0]
        df = pd.read_csv(path.join(folder, file))
        df['truck_id'] = number_id
        merge_df = pd.concat([merge_df, df], ignore_index=True)
        remove(f"{folder}/{file}")
    
    merge_df.to_csv(f"{folder}/{filename}.csv", index=False)
    if upload_csv_file in listdir(folder):
        return True

    return False

def clean_dataframe() -> pd.DataFrame:
    return ''