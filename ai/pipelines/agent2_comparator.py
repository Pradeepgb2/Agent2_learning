from pathlib import Path
from datetime import datetime
import re

# Path setup for directories
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / 'scrapers'/'data' / 'raw'
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Identify the two most recent datasets
DATASET_PREFIX = 'employees_linkedin_data_'
date_pattern = re.compile(r"(\d{4}-\d{2}-\d{2})")
files_with_dates = []


for file in RAW_DIR.glob(f"{DATASET_PREFIX}*.csv"):
    match = date_pattern.search(file.name)
    if match:
        file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
        files_with_dates.append((file, file_date))
files_with_dates.sort(key=lambda x: x[1], reverse=True)


if len(files_with_dates) < 2:
    new_file, prev_file = files_with_dates[0][0], files_with_dates[0][0]
else:
    new_file, prev_file = files_with_dates[0][0], files_with_dates[1][0]

import pandas as pd

employees_old = prev_file
employees_new =  new_file

# -------------------------
# CONFIG
# -------------------------
USECOLS = [0, 1, 2, 3, 4]  # only first 5 columns
DTYPES = {
    0: "string",
    1: "string",
    2: "string",
    3: "string",
    4: "string"
}

# -------------------------
# LOAD CSVs (FAST)
# -------------------------
old_df = pd.read_csv(
    employees_old,
    usecols=USECOLS,
    dtype=DTYPES,
    engine="c",
)

new_df = pd.read_csv(
    employees_new,
    usecols=USECOLS,
    dtype=DTYPES,
    engine="c",
)

old_df.columns = ["email_id", "name", "role", "company_name", "company_location"]
new_df.columns = ["email_id", "name", "role", "company_name", "company_location"]

# -------------------------
# CLEAN DATA (VECTORISED)
# -------------------------
for df in (old_df, new_df):
    df["email_id"] = df["email_id"].str.strip().str.lower()
    df["role"] = df["role"].str.strip()
    df["company_name"] = df["company_name"].str.strip()
    df["company_location"] = df["company_location"].str.strip().fillna("")

# -------------------------
# MERGE ONLY NEEDED COLUMNS
# -------------------------
merged = old_df[
    ["email_id", "role", "company_name", "company_location"]
].merge(
    new_df[["email_id", "role", "company_name"]],
    on="email_id",
    how="inner",
    suffixes=("_old", "_new")
)

# -------------------------
# FILTER CHANGED ROWS (VECTORIZED)
# -------------------------
company_changed = merged["company_name_old"] != merged["company_name_new"]
role_changed = merged["role_old"] != merged["role_new"]

changed_rows = merged[company_changed | role_changed]

# -------------------------
# STATUS (NO APPLY)
# -------------------------
changed_rows.loc[role_changed, "Status"] = "role changed"
changed_rows.loc[company_changed, "Status"] = "company changed"

# -------------------------
# FINAL REPORT
# -------------------------
changed_rows["Company (Location)"] = (
    changed_rows["company_name_old"]
    + " ("
    + changed_rows["company_location"].replace("", "Unknown")
    + ")"
).copy()

new_dataset = changed_rows[
    ["email_id", "Company (Location)", "role_old", "Status"]
].rename(
    columns={
        "email_id": "Email",
        "role_old": "Position"
    }
).copy()

new_dataset = new_dataset.reset_index(drop=True)
new_dataset.index += 1

new_dataset.to_csv(BASE_DIR / 'ai' / 'output' / 'employee_changes_report.csv', index=False)