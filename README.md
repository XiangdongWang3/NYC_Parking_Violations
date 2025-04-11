# 🚨 NYC Vehicle Violation Dashboard

An interactive analytics system for visualizing and querying **New York City vehicle-related violations**, powered by **Spark**, **PostgreSQL**, **Flask**, and **Streamlit**.

> **Data Source**: [NYC Open Parking and Camera Violations](https://data.cityofnewyork.us/)

---

## 📦 Features

- 📅 **Search by Date – Summary**  
  View total number of violations and total fines issued on a specific day.

- 📊 **Search by Date – Visualization**  
  Explore violation type distribution and ticket origin by state in interactive charts.

- 🔍 **Search by Summons Number**  
  Look up the detailed record for a specific summons number.

---

## ⚙️ Tech Stack

| Layer             | Technology       |
|------------------|------------------|
| Data Storage      | PostgreSQL       |
| Data Processing   | PySpark          |
| Backend API       | Flask            |
| Frontend Interface| Streamlit        |
| ETL Automation    | Python + Spark   |
| Data Source       | NYC Open Data API|

---

## 🧪 ETL Process Overview

1. **Extract**  
   - Fetched 4 million most recent records from the NYC Open Data API  
   - Approx. 1.1 GB of raw data

2. **Transform**  
   - Cleaned with PySpark: removed nulls, filled penalty fields, cast `summons_number` to string  
   - Derived weekday, time period, AM/PM, etc.  

3. **Load**  
   - Transformed data loaded into PostgreSQL using batched `to_sql()` (with chunksize)

---

## 🔗 Flask API Endpoints

| Endpoint                                             | Description                            |
|------------------------------------------------------|----------------------------------------|
| `/violations/summary?date=YYYY-MM-DD`               | Total violations and fines             |
| `/violations/by-type?date=YYYY-MM-DD`               | Violation type distribution            |
| `/violations/by-state?date=YYYY-MM-DD`              | State-wise distribution of violations  |
| `/violations/detail?summons_number=XXXXXXXXXX`      | Lookup details for a specific ticket   |

---

## 📊 Dashboard Interface (Streamlit)

> The dashboard supports flexible date search, visualization, and summons lookup.

![Dashboard Screenshot](https://via.placeholder.com/800x400.png?text=Dashboard+Preview)

---
