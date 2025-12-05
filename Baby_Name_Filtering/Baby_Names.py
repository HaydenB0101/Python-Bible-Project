import pandas as pd 
import os
import matplotlib.pyplot as plt

#print(os.getcwd())
#pd.read_csv(file_path, sep=',', header=None, names=['col1', 'col2', 'col3'])
df_1880 = pd.read_csv('/data/groups/classes/2025/fall/ds150_002/gesst9660/Bible Project/Baby_Names_1880-2022/yob1880.txt',
 sep=',', header=None, names=['Name', 'Gender', 'Count'])
df_1881 = pd.read_csv('/data/groups/classes/2025/fall/ds150_002/gesst9660/Bible Project/Baby_Names_1880-2022/yob1881.txt',
 sep=',', header=None, names=['Name', 'Gender', 'Count'])
print(df_1880)
print(df_1881)

names_df = df_1880
filenames = {}
names_df['year'] = 1880
all_years = []
for year in range(1880, 2023): #1880-2022
    filenames[f"/data/groups/classes/2025/fall/ds150_002/gesst9660/Bible Project/Baby_Names_1880-2022/yob{year}.txt"] = year
print(len(filenames))
#print(filenames)

for file, year in filenames.items():
    names_df = pd.read_csv(file, sep=',', header=None, names=['Name', 'Gender', 'Count'])
    names_df['Year'] = year
    all_years.append(names_df)
    
names_df = pd.concat(all_years, ignore_index=True)
print(names_df)
