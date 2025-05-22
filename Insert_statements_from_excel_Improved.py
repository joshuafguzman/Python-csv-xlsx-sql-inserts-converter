import pandas as pd
import os

def generate_sql_inserts(file_path, table_name, output_file="output_inserts.sql"):
    # Determine file extension and read accordingly
    file_ext = os.path.splitext(file_path)[-1].lower()
    if file_ext == '.csv':
        df = pd.read_csv(file_path)
    elif file_ext in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path, engine='openpyxl')
    else:
        raise ValueError("Unsupported file format. Use .csv or .xlsx/.xls")

    # Clean column names
    df.columns = [col.strip().replace(" ", "_").replace("-", "_") for col in df.columns]

    insert_statements = []
    for index, row in df.iterrows():
        values = []
        for val in row:
            if pd.isna(val) or val == '':
                values.append("NULL")
            elif isinstance(val, str):
                clean_val = val.replace("'", "''").strip()
                values.append(f"'{clean_val}'")
            elif isinstance(val, pd.Timestamp):
                values.append(f"'{val.strftime('%Y-%m-%d')}'")
            else:
                values.append(str(val))
        insert_stmt = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(values)});"
        insert_statements.append(insert_stmt)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(insert_statements))

    print(f"{len(insert_statements)} SQL insert statements written to {output_file}")

# === USAGE ===

# Replace with your own Excel file path and desired table name
file_path = "/Users/joshuaguzman/Downloads/archive-2/2019.csv"
table_name = "happiness_data"

# Generate SQL INSERT statements and save to file
generate_sql_inserts(file_path, table_name)

print("✅ SQL INSERT statements saved to output_inserts.sql")
