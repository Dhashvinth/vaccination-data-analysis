import os
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine


# ==========================================================
# 1. PROJECT PATH
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


# ==========================================================
# 2. FILE PATHS
# ==========================================================

files = {
    "vaccine_schedule": DATA_DIR / "vaccine-schedule-data.xlsx",
    "reported_cases": DATA_DIR / "reported-cases-data.xlsx",
    "incidence": DATA_DIR / "incidence-rate-data.xlsx",
    "vaccine_introduction": DATA_DIR / "vaccine-introduction-data.xlsx",
    "coverage": DATA_DIR / "coverage-data.xlsx"
}


# ==========================================================
# 3. LOAD EXCEL FILES
# ==========================================================

print("\nLoading Excel files...")


vaccine_schedule = pd.read_excel(
    files["vaccine_schedule"]
)

print("Vaccine schedule loaded")


reported_cases = pd.read_excel(
    files["reported_cases"]
)

print("Reported cases loaded")


incidence = pd.read_excel(
    files["incidence"]
)

print("Incidence loaded")


vaccine_introduction = pd.read_excel(
    files["vaccine_introduction"]
)

print("Vaccine introduction loaded")


coverage = pd.read_excel(
    files["coverage"]
)

print("Coverage loaded")


print("\nAll Excel files loaded successfully.")


# ==========================================================
# 4. REMOVE DUPLICATES
# ==========================================================

vaccine_schedule = vaccine_schedule.drop_duplicates()

reported_cases = reported_cases.drop_duplicates()

incidence = incidence.drop_duplicates()

vaccine_introduction = vaccine_introduction.drop_duplicates()

coverage = coverage.drop_duplicates()


print("\nDuplicate rows removed.")


# ==========================================================
# 5. CLEAN COLUMN NAMES
# ==========================================================

for df in [
    vaccine_schedule,
    reported_cases,
    incidence,
    vaccine_introduction,
    coverage
]:

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )


print("\nColumn names cleaned.")


# ==========================================================
# 6. RENAME COLUMNS
# ==========================================================

# In these datasets:
# "name" represents the country
# "antigen" represents the vaccine


coverage = coverage.rename(
    columns={
        "name": "country",
        "antigen": "vaccine"
    }
)


reported_cases = reported_cases.rename(
    columns={
        "name": "country"
    }
)


incidence = incidence.rename(
    columns={
        "name": "country"
    }
)


vaccine_schedule = vaccine_schedule.rename(
    columns={
        "name": "country",
        "antigen": "vaccine"
    }
)


vaccine_introduction = vaccine_introduction.rename(
    columns={
        "name": "country",
        "antigen": "vaccine"
    }
)


print("\nColumns renamed successfully.")


print("\nCoverage columns:")

print(
    coverage.columns.tolist()
)


# ==========================================================
# 7. CHECK MISSING VALUES
# ==========================================================

print("\n========== MISSING VALUES ==========")


print("\nCoverage:")

print(
    coverage.isnull().sum()
)


print("\nReported Cases:")

print(
    reported_cases.isnull().sum()
)


print("\nIncidence:")

print(
    incidence.isnull().sum()
)


# ==========================================================
# 8. CHECK COVERAGE VALUES
# ==========================================================

print("\n========== COVERAGE CHECK ==========")


print(
    "\nValues above 100%:",
    (coverage["coverage"] > 100).sum()
)


print(
    "Values above 200%:",
    (coverage["coverage"] > 200).sum()
)


# ==========================================================
# 9. CREATE COVERAGE STATUS
# ==========================================================

coverage["coverage_status"] = "Normal"


coverage.loc[
    coverage["coverage"] > 100,
    "coverage_status"
] = "Above 100%"


coverage.loc[
    coverage["coverage"] > 200,
    "coverage_status"
] = "Extreme"


# ==========================================================
# 10. CREATE CLEAN COVERAGE DATASET
# ==========================================================

coverage_clean = coverage[
    coverage["coverage"] <= 200
].copy()


print(
    "\nCoverage cleaning completed."
)


# ==========================================================
# 11. BASIC DATASET INFORMATION
# ==========================================================

print("\n========== DATASET INFORMATION ==========")


print(
    "\nNumber of countries:",
    coverage_clean["country"].nunique()
)


print(
    "Year range:",
    coverage_clean["year"].min(),
    "to",
    coverage_clean["year"].max()
)


print(
    "Number of vaccines:",
    coverage_clean["vaccine"].nunique()
)


# ==========================================================
# 12. AVERAGE VACCINATION COVERAGE
# ==========================================================

average_coverage = (
    coverage_clean[
        "coverage"
    ].mean()
)


print("\n========== AVERAGE COVERAGE ==========")


print(
    "Average vaccination coverage:",
    average_coverage
)


# ==========================================================
# 13. AVERAGE COVERAGE BY VACCINE
# ==========================================================

coverage_by_vaccine = (
    coverage_clean
    .groupby(
        "vaccine"
    )[
        "coverage"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
)


print("\n========== COVERAGE BY VACCINE ==========")


print(
    coverage_by_vaccine
)


# ==========================================================
# 14. AVERAGE COVERAGE BY YEAR
# ==========================================================

coverage_by_year = (
    coverage_clean
    .groupby(
        "year"
    )[
        "coverage"
    ]
    .mean()
)


print("\n========== COVERAGE BY YEAR ==========")


print(
    coverage_by_year
)


# ==========================================================
# 15. AVERAGE COVERAGE BY COUNTRY
# ==========================================================

coverage_by_country = (
    coverage_clean
    .groupby(
        "country"
    )[
        "coverage"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
)


print("\n========== TOP 10 COUNTRIES ==========")


print(
    coverage_by_country.head(10)
)


print("\n========== BOTTOM 10 COUNTRIES ==========")


print(
    coverage_by_country.tail(10)
)


# ==========================================================
# 16. TOTAL REPORTED CASES BY DISEASE
# ==========================================================

cases_by_disease = (
    reported_cases
    .groupby(
        "disease"
    )[
        "cases"
    ]
    .sum()
    .sort_values(
        ascending=False
    )
)


print("\n========== CASES BY DISEASE ==========")


print(
    cases_by_disease
)


# ==========================================================
# 17. TOTAL REPORTED CASES BY YEAR
# ==========================================================

cases_by_year = (
    reported_cases
    .groupby(
        "year"
    )[
        "cases"
    ]
    .sum()
)


print("\n========== CASES BY YEAR ==========")


print(
    cases_by_year
)


# ==========================================================
# 18. AVERAGE INCIDENCE RATE BY DISEASE
# ==========================================================

incidence_by_disease = (
    incidence
    .groupby(
        "disease"
    )[
        "incidence_rate"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
)


print("\n========== INCIDENCE BY DISEASE ==========")


print(
    incidence_by_disease
)


# ==========================================================
# 19. COVERAGE BY COUNTRY AND YEAR
# ==========================================================

vaccination_country_year = (
    coverage_clean
    .groupby(
        [
            "country",
            "year"
        ]
    )[
        "coverage"
    ]
    .mean()
    .reset_index()
)


print(
    "\n========== COVERAGE BY COUNTRY AND YEAR =========="
)


print(
    vaccination_country_year.head()
)


# ==========================================================
# 20. INCIDENCE BY COUNTRY AND YEAR
# ==========================================================

incidence_country_year = (
    incidence
    .groupby(
        [
            "country",
            "year"
        ]
    )[
        "incidence_rate"
    ]
    .mean()
    .reset_index()
)


print(
    "\n========== INCIDENCE BY COUNTRY AND YEAR =========="
)


print(
    incidence_country_year.head()
)


# ==========================================================
# 21. COMBINE COVERAGE AND INCIDENCE
# ==========================================================

vaccination_disease_analysis = (
    vaccination_country_year.merge(
        incidence_country_year,
        on=[
            "country",
            "year"
        ],
        how="inner"
    )
)


print(
    "\n========== VACCINATION VS INCIDENCE =========="
)


print(
    vaccination_disease_analysis.head()
)


# ==========================================================
# 22. CORRELATION
# ==========================================================

correlation = (
    vaccination_disease_analysis[
        [
            "coverage",
            "incidence_rate"
        ]
    ].corr()
)


print("\n========== CORRELATION ==========")


print(
    correlation
)


# ==========================================================
# 23. LOAD DATABASE DETAILS FROM .ENV
# ==========================================================

load_dotenv()


username = os.getenv(
    "DB_USERNAME"
)

password = os.getenv(
    "DB_PASSWORD"
)

database = os.getenv(
    "DB_NAME"
)


# ==========================================================
# 24. CONNECT TO MYSQL
# ==========================================================

engine = create_engine(
    f"mysql+pymysql://"
    f"{username}:{password}"
    f"@localhost/{database}"
)


print(
    "\nConnected to MySQL."
)


# ==========================================================
# 25. SEND DATA TO MYSQL
# ==========================================================

print(
    "\nUploading coverage_clean..."
)


coverage_clean.to_sql(
    "coverage_clean",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)


print(
    "coverage_clean uploaded."
)


print(
    "\nUploading reported_cases..."
)


reported_cases.to_sql(
    "reported_cases",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)


print(
    "reported_cases uploaded."
)


print(
    "\nUploading incidence..."
)


incidence.to_sql(
    "incidence",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)


print(
    "incidence uploaded."
)


print(
    "\nUploading vaccine_introduction..."
)


vaccine_introduction.to_sql(
    "vaccine_introduction",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)


print(
    "vaccine_introduction uploaded."
)


print(
    "\nUploading vaccine_schedule..."
)


vaccine_schedule.to_sql(
    "vaccine_schedule",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)


print(
    "vaccine_schedule uploaded."
)


print(
    "\nUploading vaccination_disease_analysis..."
)


vaccination_disease_analysis.to_sql(
    "vaccination_disease_analysis",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)


print(
    "vaccination_disease_analysis uploaded."
)


# ==========================================================
# 26. FINISHED
# ==========================================================

print("\n======================================")
print("DATA ANALYSIS COMPLETED SUCCESSFULLY")
print("======================================")


print(
    "\nTables available in MySQL:"
)


print(
    "1. coverage_clean"
)

print(
    "2. reported_cases"
)

print(
    "3. incidence"
)

print(
    "4. vaccine_introduction"
)

print(
    "5. vaccine_schedule"
)

print(
    "6. vaccination_disease_analysis"
)


print(
    "\nData is ready for Power BI."
)