import pandas as pd

# Example: two matching DataFrames
df1 = pd.read_excel("qft_10_main.xlsx", dtype={'Binary': str})
df2 = pd.read_excel("qft_10_remote_main.xlsx", dtype={'Binary': str})

# Merge them into one DataFrame
merged_df = pd.concat([df1, df2], ignore_index=True)
merged_df.to_excel("qft_10_merged_updated.xlsx", index=False)
