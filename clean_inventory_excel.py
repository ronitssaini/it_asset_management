import pandas as pd
import argparse

# Define expected columns for each sheet
desktop_columns = [
    "Company Name", "Device Type", "MAKE", "Serial No.", "Processor", "Hard disk", "Ram", "Monitor", "Location",
    "OS Version", "IP address", "Subnet Mask", "Purchase Date", "Additional Device", "Emp. Code", "Name", "Function", "Role", "Remarks"
]
server_columns = [
    "Company Name", "Typer", "MAKE", "Serial No.", "Processor Typer", "Processor", "Total Processo Core", "Internal Hard Disk",
    "Disk Type", "Qty", "Raid", "Ram", "Network Card", "HBA Card", "Location", "OS Version", "IP address", "Subnet Mask", "Purchase Date"
]
switch_columns = [
    "Company Name", "Model", "MAKE", "Serial No.", "No. of Ports", "OS Version", "IP address", "Subnet Mask", "Purchase Date", "Additional Device", "Remarks"
]

required_columns = {
    "Desktop": ["Serial No.", "Company Name", "Device Type"],
    "Server": ["Serial No.", "Company Name"],
    "Switches": ["Serial No.", "Company Name"]
}

sheet_columns = {
    "Desktop": desktop_columns,
    "Server": server_columns,
    "Switches": switch_columns
}

def clean_sheet(df, sheet_name):
    # Standardize columns
    df = df.rename(columns=lambda x: x.strip() if isinstance(x, str) else x)
    # Keep only expected columns
    expected = sheet_columns[sheet_name]
    df = df[[col for col in expected if col in df.columns]]
    # Drop rows with missing required fields
    req = required_columns[sheet_name]
    df = df.dropna(subset=req)
    # Remove duplicates by Serial No.
    df = df.drop_duplicates(subset=["Serial No."])
    return df

def main():
    parser = argparse.ArgumentParser(description="Clean and standardize IT asset inventory Excel file.")
    parser.add_argument('--input', required=True, help='Path to raw Excel file')
    parser.add_argument('--output', required=True, help='Path to cleaned Excel file')
    args = parser.parse_args()

    xls = pd.ExcelFile(args.input)
    cleaned = {}
    for sheet in ["Desktop", "Server", "Switches"]:
        if sheet in xls.sheet_names:
            print(f"[INFO] Cleaning sheet: {sheet}")
            df = pd.read_excel(xls, sheet_name=sheet, skiprows=1)
            cleaned_df = clean_sheet(df, sheet)
            print(f"[INFO] {sheet}: {len(cleaned_df)} rows after cleaning.")
            cleaned[sheet] = cleaned_df
        else:
            print(f"[INFO] Sheet '{sheet}' not found, skipping.")
    if not cleaned:
        print("[ERROR] No valid sheets found. Exiting.")
        return
    with pd.ExcelWriter(args.output) as writer:
        for sheet, df in cleaned.items():
            df.to_excel(writer, sheet_name=sheet, index=False)
    print(f"[INFO] Cleaned file written to {args.output}")

if __name__ == "__main__":
    main() 