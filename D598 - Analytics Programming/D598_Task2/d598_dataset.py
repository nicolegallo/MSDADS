import pandas as pd
import numpy as np

# 1.IMPORT the dataset from "D598 Data Set.xlsx" into a data frame called df
try:
    df = pd.read_excel("D598_Data_Set.xlsx", sheet_name="1-150 V2")
except Exception as e:
    raise FileNotFoundError(f"Error loading Excel file: {e}")

# 2.IDENTIFY any duplicate rows in df
# CALL df.duplicated() to detect duplicates
# STORE duplicates in a separate data frame if needed
duplicates = df[df.duplicated()]
print("Duplicate rows found:", len(duplicates))
# REMOVE duplicates if any
if not duplicates.empty:
    df = df.drop_duplicates()
    print("Duplicates removed.")

# 3.GROUP df BY "Business State"
required_columns = [
    'Total Revenue', 'Total Long-term Debt', 'Total Equity',
    'Total Liabilities', 'Debt to Equity', 'Profit Margin'
]

# CALCULATE descriptive statistics (mean, median, min, max)
# PRINT/STORE this grouped result as a new data frame called df_by_state
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    print(f"Warning: Missing columns for grouping: {missing_cols}")
    df_by_state = None
else:
    df_by_state = df.groupby("Business State")[required_columns].agg(['mean', 'median', 'min', 'max'])
    print("Grouped Statistics by State:")
    print(df_by_state.head())

# 4.FILTER df to find rows where "Debt to Equity" is less than 0
# STORE/PRINT this filtered result as df_negative_dte
if "Debt to Equity" in df.columns:
    df_negative_dte = df[df["Debt to Equity"] < 0]
    print("Businesses with Negative Debt to Equity:")
    print(df_negative_dte[["Business ID", "Business State", "Debt to Equity"]].head())
else:
    print("Warning: 'Debt to Equity' column not found.")
    df_negative_dte = pd.DataFrame()

# 5. CREATE a new column "Debt to Income Ratio"
# CALCULATE by dividing "Total Long-term Debt" by "Total Revenue" for each row
if "Total Revenue" in df.columns and "Total Long-term Debt" in df.columns:
    df["Debt to Income Ratio"] = np.where(
        df["Total Revenue"] == 0,
        np.nan, # If Total Revenue is 0, assign NaN to avoid division by zero
        df["Total Long-term Debt"] / df["Total Revenue"]
    )
else:
    print("Warning: Missing columns for Debt to Income Ratio calculation.")
    df["Debt to Income Ratio"] = np.nan


# 6.CONCATENATE the new column to the original df
# STORE the result as df_combined
df_combined = df.copy()

# 7.GENERATE updated dataset as output (e.g., export or prepare for reporting)
df_combined.to_excel("Updated_D598_Data_Set.xlsx", index=False)

print("Updated Dataset with Debt-to-Income Ratio:")
print(df_combined.head())
