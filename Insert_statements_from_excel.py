import pandas as pd
import os

def excel_or_csv_to_sql_insert(file_path, table_name):
    # Detect file extension
    _, ext = os.path.splitext(file_path.lower())

    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path, engine="openpyxl")
    else:
        raise ValueError("Unsupported file type. Please use CSV or Excel (.xlsx/.xls).")

    # Format column names
    columns = [f"`{col}`" for col in df.columns]
    column_str = ", ".join(columns)

    insert_statements = []

    for _, row in df.iterrows():
        values = []
        for val in row:
            if pd.isna(val):
                values.append("NULL")
            elif isinstance(val, str):
                safe_val = val.replace("'", "''")  # escape single quotes
                values.append(f"'{safe_val}'")
            else:
                values.append(str(val))
        value_str = ", ".join(values)
        statement = f"INSERT INTO {table_name} ({column_str}) VALUES ({value_str});"
        insert_statements.append(statement)

    return insert_statements

# === USAGE ===
# Replace with your own Excel file path and desired table name
file_path = "/Users/joshuaguzman/Downloads/archive-2/2019.csv"
table_name = "happiness_data"

# Generate SQL statements
sql_statements = excel_or_csv_to_sql_insert(file_path, table_name)

# Save to file
with open("output.sql", "w", encoding="utf-8") as f:
    for stmt in sql_statements:
        f.write(stmt + "\n")

print("✅ SQL INSERT statements saved to output.sql")
