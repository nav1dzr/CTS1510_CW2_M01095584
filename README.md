# 📦 CTS1510 Coursework 2 – Data Migration & Metadata Processing  
Python • Pandas • SQLite • Data Cleaning

This project is my **final version** for CTS1510 Coursework 2.  
It processes CSV metadata files, cleans the fields, transforms the data, and inserts the results into a structured SQLite database.

The project demonstrates:
- Data cleaning  
- Schema transformation  
- Data validation  
- SQL table creation  
- CSV → Database migration  
- Python modular design  

---

## 🚀 Features

### ✔️ 1. CSV Metadata Loading
Reads metadata CSV files containing dataset information such as:
- dataset name  
- rows  
- uploaded_by  
- upload_date  
- dataset_id  

### ✔️ 2. Data Cleaning & Transformation
The script:
- Removes unnecessary columns  
- Renames fields to match DB schema  
- Ensures consistent formatting  
- Keeps only valid fields for final table insertion  

### ✔️ 3. SQLite Database Insertion
Automatically inserts cleaned metadata into:
