import pandas as pd
import string

###filtering unique names from the csv file###
df = pd.read_csv('Person_Data/BibleData-Person.csv')

# list of all unique names from the 'person_name' column
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

#print(filtered_text[:500])  # Print the first 500 characters of the filtered text



# Step 1 — Clean the filtered_text (lowercase + remove punctuation)
clean_text = filtered_text.lower()

for p in string.punctuation:
    clean_text = clean_text.replace(p, " ")

# Turn into list of words
words = clean_text.split()

def count_names():
    name_counts = {}

    for name in unique_names:
        lower_name = name.lower()
        count = words.count(lower_name)
        name_counts[name] = count  

    return name_counts

name_counts = count_names()
print(name_counts)
