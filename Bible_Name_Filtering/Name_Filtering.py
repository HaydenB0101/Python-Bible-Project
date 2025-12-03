import pandas as pd
import re
import os

###filtering unique names from the csv file###
df = pd.read_csv('Person_Data/BibleData-Person.csv')
# df = pd.read_csv('Bible_Name_Filtering/Person_Data/BibleData-Person.csv')

# list of all unique names from the 'person_name' column
unique_names = df['person_name'].dropna().unique().tolist()
print(unique_names)

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
with open('Bible_Name_Filtering/Person_Data/kjb.txt', 'r', encoding='utf-8') as f:
    kjb_text = f.read()
filtered_text = keep_substring(kjb_text, "1:1 In the beginning God created the heaven and the earth.", where="after", include=True).strip()
filtered_text = keep_substring(filtered_text,"*** END OF THE PROJECT GUTENBERG EBOOK THE KING JAMES VERSION OF THE BIBLE ***" , where="before", include=False).strip()

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

print(name_counts.head(20))