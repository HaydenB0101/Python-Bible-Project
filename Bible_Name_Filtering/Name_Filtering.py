import pandas as pd
import re

# filtering unique names from the csv file
df = pd.read_csv('Person_Data/BibleData-Person.csv')

# clean unique names
unique_names = (
    df['person_name']
    .dropna()
    .astype(str)
    .str.strip()
    .replace('', pd.NA)
    .dropna()
    .unique()
    .tolist()
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
with open('Person_Data/kjb.txt', 'r', encoding='utf-8') as f:
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

# dataframe of name frequency
df_counts = pd.DataFrame({'name': unique_names, 'count': counts})
df_counts = df_counts.sort_values(by='count', ascending=False).reset_index(drop=True)
df_counts['rank'] = df_counts['count'].rank(method='dense', ascending=False).astype(int)

df_counts.to_csv('Person_Data/name_counts.csv', index=False)
print("The file has been created (finally)")