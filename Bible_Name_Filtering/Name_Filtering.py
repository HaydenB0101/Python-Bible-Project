import pandas as pd
import re
import os

# minimum number of mentions to keep a name
MIN_COUNT = 10

# filtering unique names from the csv file
# read person data
df = pd.read_csv('Bible_Name_Filtering/Person_Data/BibleData-Person.csv')

# clean person_name in the dataframe so counts by person_id align with our unique_names
df['person_name'] = df['person_name'].astype(str).str.strip()

# clean unique names
unique_names = (
    df['person_name']
    .astype(str)
    .str.strip()
    .replace('', pd.NA)
    .dropna()
    .unique()
    .tolist()
)

# compute how many distinct person_id values exist for each cleaned name
# this gives the number of distinct people who had that given name
person_counts = (
    df.dropna(subset=['person_name'])
      .groupby('person_name')['person_id']
      .nunique()
      .to_dict()
)

# Reading from kjb.txt and filtering
def keep_substring(superset, sub, where, include):
    if sub not in superset:
        raise ValueError(f"'{sub}' not found in superset.")
    if where not in ["before", "after"]:
        raise ValueError("Argument 'where' must be either 'before' or 'after'.")
    index = superset.find(sub)
    if where == "before":
        return superset[:index + len(sub)] if include else superset[:index]
    else:
        return superset[index:] if include else superset[index + len(sub):]

# Import and clean KJV
with open('Bible_Name_Filtering/Person_Data/kjb.txt', 'r', encoding='utf-8') as f:
    kjb_text = f.read()

filtered_text = keep_substring(
    kjb_text,
    "1:1 In the beginning God created the heaven and the earth.",
    where="after",
    include=True
).strip()

filtered_text = keep_substring(
    filtered_text,
    "*** END OF THE PROJECT GUTENBERG EBOOK THE KING JAMES VERSION OF THE BIBLE ***",
    where="before",
    include=False
).strip()

# count name occurrences
counts = []

for name in unique_names:
    clean_name = str(name).strip()
    if not clean_name:
        counts.append(0)
        continue

    # Case 1: Multi-word names — match full phrase
    if " " in clean_name:
        pattern = r"(?<!\w)" + re.escape(clean_name) + r"(?!\w)"

    # Case 2: Very short names — avoid English words
    elif len(clean_name) <= 3:
        pattern = (
            r"(?<!\w)" +
            re.escape(clean_name) +
            r"(?=[,.;:!? )\"])"  # careful endings
        )

    # Case 3: Normal single-word names — whole-word match
    else:
        pattern = r"\b" + re.escape(clean_name) + r"\b"

    matches = re.findall(pattern, filtered_text, flags=re.IGNORECASE)
    counts.append(len(matches))
    # (Only total match counts are kept)

# dataframe of name frequency
df_counts = pd.DataFrame({
    'name': unique_names,
    'count': counts,
})
df_counts = df_counts.sort_values(by='count', ascending=False).reset_index(drop=True)

# Map name -> number of distinct person_id values (people who had that name)
df_counts['people_count'] = df_counts['name'].map(lambda n: person_counts.get(n, 0))

# Trim names mentioned fewer than MIN_COUNT (10) times
df_counts = df_counts[df_counts['count'] >= MIN_COUNT].reset_index(drop=True)

output_path = 'Bible_Name_Filtering/Data_Output/name_counts.csv'
df_counts.to_csv(output_path, index=False)
print(f"Saved {len(df_counts)} names with >= {MIN_COUNT} occurrences to {output_path}")