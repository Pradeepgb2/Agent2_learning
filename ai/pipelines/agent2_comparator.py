import pandas as pd

employees_old = r"C:\Users\Narasimha\Desktop\ai_recruiting_infrastructure_agent2\scrapers\data\raw\employees_past_week.csv"
employees_new = r"C:\Users\Narasimha\Desktop\ai_recruiting_infrastructure_agent2\scrapers\data\raw\employees_present_week.csv"

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
changed_rows["Status"] = "role changed"
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
)

new_dataset = new_dataset.reset_index(drop=True)
new_dataset.index += 1

new_dataset.to_csv(r"C:\Users\Narasimha\Desktop\Agent2_sample\ai\output\employee_changes_report.csv")
