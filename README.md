# Vaccination Data Analysis

## Project Overview

This project analyzes global vaccination coverage and disease data using **Python, MySQL, and Power BI**.

Python is used for data cleaning and analysis, MySQL is used to store the processed data, and Power BI is used to create an interactive dashboard.

## Technologies Used

- Python
- Pandas
- MySQL
- SQLAlchemy
- Power BI
- Excel

## Project Workflow

```text
Excel Data
    ↓
Python Data Cleaning
    ↓
Exploratory Data Analysis
    ↓
MySQL Database
    ↓
Power BI Dashboard
```

## Analysis Performed

The project includes:

- Vaccination coverage analysis by country
- Vaccination coverage analysis by year
- Vaccination coverage analysis by vaccine
- Analysis of reported disease cases
- Analysis of disease incidence rates
- Comparison of vaccination coverage and disease incidence

## Data Cleaning

The datasets were cleaned using Python and Pandas by:

- Removing duplicate records
- Standardizing column names
- Checking missing values
- Identifying unusual vaccination coverage values
- Removing extreme coverage values above 200%

## Power BI Dashboard

The cleaned data was connected to Power BI to visualize vaccination coverage and disease trends.

<img width="604" height="337" alt="dashboard" src="https://github.com/user-attachments/assets/34078661-98c0-43b8-a7e6-9bea51427717" />



## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Create a `.env` file with your MySQL credentials:

```text
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_NAME=vaccination_analysis
```

Run the project:

```bash
python app.py
```

## Author

**Dhashvinth Bashkar**
