# Python-Bible-Project
This project analyzes the frequency and distribution of names found in the Bible. Multiple datasets and scripts contributed by classmates are used to compare the most common names, explore gender-based trends, and visualize patterns across different sources.

This README includes placeholders so details can be filled in once all group members upload their files.

---

## 📁 Project Structure
```
project/
├── Baby_Name_Filtering/
│   ├── plots/
│   │   ├── Aaron_Frequency.png
│   │   ├── David_Frequency.png
│   │   ├── Eve_Frequency.png
│   │   ├── Jacob_Frequency.png
│   │   ├── Jesus_Frequency.png
│   │   ├── Judah_Frequency.png
│   │   ├── Mary_Frequency.png
│   │   ├── Moses_Frequency.png
│   │   ├── Saul_Frequency.png
│   │   └── Top10Names.png
│   ├── Baby_Names.py
│   ├── yob[1880].txt
│   ├── yob[1881...2019].txt
│   └── yob[2020].txt
├── Bible_Name_Filtering/
│   ├── Data_Output/
│   │   └── name_counts.csv
│   ├── Person_Data/
│   │   ├── BibleData-Person.csv
│   │   ├── kjb.txt
│   │   └── LICENSE
│   └── Name_Filtering.py
└── README.md
```
---

## 🧰 Features

- Loads and consolidates U.S. baby name data (1880–2022)  
- Computes total baby counts per year and individual name trends  
- Plots line charts for overall and specific name frequencies  
- Reads and cleans Bible person data and full KJV text  
- Splits Bible text into books for per-book analysis  
- Counts unique male and female names per book  
- Generates **Top 10** male and female names and books  
- Produces bar charts comparing male vs female names per book  
- Exports cleaned datasets and name count summaries to CSV  
- Handles filtering and minimum occurrence thresholds for names  

---

## 📊 Data Sources

| Dataset Name | Description |
|--------------|-------------|
| BibleData-Person.csv  | Primary dataset           |
| kjb.txt               | Text for Bible            |
| yob[1880...2022].txt  | Names and year of birth   |

---

## Group Members

Hayden Boeckmann

Tyler Gess

Logan Haack

Marley Schermerhorn

Melinda Wilson

---

## 🚀 How to Run the Project

1. Install dependencies (if needed):

```bash
pip install pandas matplotlib
```

2. Run the scripts:

```bash
# To analyze baby names
python Baby_Name_Filtering/Baby_Names.py
# To analyze Bible names
python Bible_Name_Filtering/Name_Filtering.py
```
