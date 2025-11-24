import pandas as pd
import re

###filtering unique names from the csv file###
df = pd.read_csv('Person_Data/BibleData-Person.csv')

# list of all unique names from 'person_name' gnoring blank(NaN) entries
unique_names = df['person_name'].dropna().unique().tolist()
#print(unique_names)

###Reading from kjb.txt and filtering ###
# code from Assignment 5
def keep_substring(superset, sub, where, include):
    # Check if substring is present
    if sub not in superset:
        raise ValueError(f"'{sub}' not found in superset.")
    # Check for valid 'where' argument
    if where not in ["before", "after"]:
        raise ValueError("Argument 'where' must be either 'before' or 'after'.")
    # Find index of substring
    index = superset.find(sub)
    # Slice depending on the arguments
    if where == "before":
        if include:
            return superset[:index + len(sub)]
        else:
            return superset[:index]
    else:  # where == "after"
        if include:
            return superset[index:]
        else:
            return superset[index + len(sub):]

# Import kjb.txt and clean it
with open('Person_Data/kjb.txt', 'r', encoding='utf-8') as f:
    kjb_text = f.read()
filtered_text = keep_substring(kjb_text, "1:1 In the beginning God created the heaven and the earth.", where="after", include=True).strip()
filtered_text = keep_substring(filtered_text,"*** END OF THE PROJECT GUTENBERG EBOOK THE KING JAMES VERSION OF THE BIBLE ***" , where="before", include=False).strip()

# count how often each name appears (case-insensitive, whole-word)
counts = []
for name in unique_names:
    # check if name is a string and skip NaN
    if pd.isna(name):
        counts.append(0)
        continue
    #look for when name is by itself and not part of a word
    pattern = r"\b" + re.escape(str(name)) + r"\b"
    matches = re.findall(pattern, filtered_text, flags=re.IGNORECASE)
    #add to counts list
    counts.append(len(matches))

# dataframe of name frequency
df_counts = pd.DataFrame({'name': unique_names,'count': counts})
df_counts = df_counts.sort_values(by='count', ascending=False).reset_index(drop=True)
df_counts['rank'] = df_counts['count'].rank(method='dense', ascending=False).astype(int)

# Save results to CSV
df_counts.to_csv('Person_Data/name_counts.csv', index=False)
printf("The file has been created (finally)")