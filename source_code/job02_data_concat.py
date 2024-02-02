import pandas as pd
import glob


file_path = glob.glob("../crawling_data/*")

df = pd.DataFrame()

for file in file_path:
    df_temp = pd.read_csv(file, index_col=False)
    df_temp.columns = ["titles", "reviews"]
    df_temp.dropna(inplace=True)
    df = pd.concat([df, df_temp], axis="rows", ignore_index=True)

df.drop_duplicates(inplace=True)

print(df.info())
print(len(df))

df.to_csv("../learning_data/reviews_kinolights.csv", index=False)
