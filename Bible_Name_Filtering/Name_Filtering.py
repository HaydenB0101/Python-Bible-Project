import pandas as pd
import re
import os
import matplotlib.pyplot as plt

###filtering unique names from the csv file###
# df = pd.read_csv('Person_Data/BibleData-Person.csv')
df = pd.read_csv('Bible_Name_Filtering/Person_Data/BibleData-Person.csv')

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
        return superset[:index + len(sub)] if include else superset[:index]
    else:
        return superset[index:] if include else superset[index + len(sub):]

# Import and clean KJV
with open('Bible_Name_Filtering/Person_Data/kjb.txt', 'r', encoding='utf-8') as f:
    kjb_text = f.read()

print(filtered_text[:500])  # Print the first 500 characters of the filtered text

bible_books = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
    "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
    "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel",
    "Amos", "Obadiah", "Jonah", "Micah", "Nahum",
    "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
    "Ephesians", "Philippians", "Colossians", "1 Thessalonians",
    "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus",
    "Philemon", "Hebrews", "James", "1 Peter",
    "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation"
]

def split_into_books(text, book_names):
    book_text = {}
    escaped = [re.escape(b) for b in book_names]
    pattern = r"(" + "|".join(escaped) + r")\s+"
    parts = re.split(pattern, text)
    book_text = {}
    for i in range(1, len(parts), 2):
        book = parts[i]
        content = parts[i+1]
        book_text[book] = content
    return book_text

book_sections = split_into_books(filtered_text, bible_books)
# print(book_sections.keys())
females = df[df["sex"] == "female"]["person_name"].dropna().unique().tolist()
female_counts = {}
for book, text in book_sections.items():
    found = set()
    for name in females:
        if re.search(rf"\b{name}\b", text):
            found.add(name)
    female_counts[book] = len(found)
# print("Female dictionary: \n", female_counts)
top10_females = pd.Series(female_counts).sort_values(ascending=False).head(10)
print("Top 10 books with most (unique) female names:\n", top10_females)

males = df[df["sex"] == "male"]["person_name"].dropna().unique().tolist()
male_counts = {}
for book, text in book_sections.items():
    found = set()
    for name in males:
        if re.search(rf"\b{name}\b",text):
            found.add(name)
    male_counts[book] = len(found)
# print("Male dictionary: \n", male_counts)
top10_males = pd.Series(male_counts).sort_values(ascending=False).head(10)
print("Top 10 books with most (unique) male names:\n", top10_males)

most_popular_names = {}

name_counts = df.groupby("person_name")["name_instance"].count().sort_values(ascending=False)

counts_df = pd.DataFrame({
    "female_unique_names": pd.Series(female_counts),
    "male_unique_names":pd.Series(male_counts)
})
name_counts.to_csv("name_counts.csv", header=["count"])
counts_df.to_csv("book_gender_name_counts.csv")
top10_females.to_csv("top10_books_female_names.csv", header=["unique_female_names"])
top10_males.to_csv("top10_books_male_names.csv", header=["unique_male_names"])

new_names_vs_books_df = pd.read_csv("book_gender_name_counts.csv", index_col=0)

plt.figure(figsize=(12, 6))
new_names_vs_books_df.plot(kind="bar", figsize=(14, 7))
plt.title("Unique Male vs Female Names per Book")
plt.ylabel("Count of Unique Names")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
top10_males.plot(kind="bar", color="steelblue")
plt.title("Top 10 Most Frequent Male Names in the Bible")
plt.xlabel("Name")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
top10_females.plot(kind="bar", color="mediumvioletred")
plt.title("Top 10 Most Frequent Female Names in the Bible")
plt.xlabel("Name")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

print(name_counts.head(20))
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
