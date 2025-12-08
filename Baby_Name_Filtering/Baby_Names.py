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
#testing of the file path

names_df = df_1880
filenames = {}
names_df['year'] = 1880
all_years = []
for year in range(1880, 2023): #1880-2022
    filenames[f"/data/groups/classes/2025/fall/ds150_002/gesst9660/Bible Project/Baby_Names_1880-2022/yob{year}.txt"] = year
print(len(filenames))
#print(filenames)
#creates dictionary of the data per year

for file, year in filenames.items():
    names_df = pd.read_csv(file, sep=',', header=None, names=['Name', 'Gender', 'Count'])
    names_df['Year'] = year
    all_years.append(names_df)
    
names_df = pd.concat(all_years, ignore_index=True)
print(names_df)
#DataFrame of all data over the years

# Create plot for total population
count_total = []
for year in range(1880, 2023):
    temp = names_df[names_df['Year']==year]
    count_total.append(temp['Count'].sum())

plt.plot(names_df['Year'].unique(), count_total, color='orange', linewidth=2, markersize=1)
plt.xlabel('Year')
plt.ylabel('# of Babies')
plt.title('Frequency of names from 1880-2022 (U.S.)')
plt.savefig('Baby_Name_Frequency.png')
plt.show()

# Create plot for specific person
Mary_df = names_df[names_df['Name']=='Mary']
MaryF_df = Mary_df[Mary_df['Gender']=='F']
print(MaryF_df)
print(MaryF_df['Count'].max())
max_mary = MaryF_df[MaryF_df['Count']==MaryF_df['Count'].max()]
print(max_mary)
plt.plot(MaryF_df['Year'], MaryF_df['Count'], color='orange', linewidth=2, markersize=1)
plt.xlabel('Year')
plt.ylabel('Babies named Mary')
plt.title('Frequency of Mary from 1880-2022 (U.S.)')
plt.savefig('Mary_Frequency.png')

Mary_sum = Mary_df['Count'].sum()
print("\n")
print(f"Total babies names Mary: {Mary_sum}")

plt.show()