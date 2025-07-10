import pandas as pd
from datetime import datetime
from backend.models.asset import Asset

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
    df = df.rename(columns=lambda x: x.strip() if isinstance(x, str) else x)
    expected = sheet_columns[sheet_name]
    df = df[[col for col in expected if col in df.columns]]
    req = required_columns[sheet_name]
    df = df.dropna(subset=req)
    df = df.drop_duplicates(subset=["Serial No."])
    return df

def clean_and_parse_inventory(file_path: str):
    """Clean and parse all relevant sheets from inventory Excel for backend upload."""
    xls = pd.ExcelFile(file_path)
    assets = []
    for sheet in ["Desktop", "Server", "Switches"]:
        if sheet in xls.sheet_names:
            print(f"[DEBUG] Cleaning and parsing sheet: {sheet}")
            df = pd.read_excel(xls, sheet_name=sheet, skiprows=1)
            cleaned_df = clean_sheet(df, sheet)
            print(f"[DEBUG] {sheet}: {len(cleaned_df)} rows after cleaning.")
            if sheet == "Desktop":
                assets.extend(_process_computers(cleaned_df))
            elif sheet == "Server":
                assets.extend(_process_servers(cleaned_df))
            elif sheet == "Switches":
                assets.extend(_process_switches(cleaned_df))
        else:
            print(f"[DEBUG] Sheet '{sheet}' not found, skipping.")
    return assets

def _process_computers(df):
    """Process desktop/laptop rows"""
    assets = []
    for _, row in df.iterrows():
        assets.append(Asset(
            company_name=row.get("Company Name"),
            device_type=row.get("Device Type"),
            make=row.get("MAKE"),
            serial_number=row.get("Serial No."),
            processor=row.get("Processor"),
            hard_disk=row.get("Hard disk"),
            ram=row.get("Ram"),
            monitor=row.get("Monitor"),
            location=row.get("Location"),
            os_version=row.get("OS Version"),
            ip_address=row.get("IP address"),
            subnet_mask=row.get("Subnet Mask"),
            purchase_date=_parse_date(row.get("Purchase Date")),
            additional_device=row.get("Additional Device"),
            employee_code=str(row.get("Emp. Code")) if pd.notna(row.get("Emp. Code")) else None,
            employee_name=row.get("Name"),
            function=row.get("Function"),
            role=row.get("Role"),
            remarks=row.get("Remarks", "")
        ))
    return assets

def _process_servers(df):
    """Process server rows"""
    assets = []
    for _, row in df.iterrows():
        assets.append(Asset(
            company_name=row.get("Company Name"),
            device_type="Server",
            typer=row.get("Typer"),
            make=row.get("MAKE"),
            serial_number=row.get("Serial No."),
            processor_type=row.get("Processor Typer"),
            processor=row.get("Processor"),
            total_processor_core=row.get("Total Processo Core"),
            internal_hard_disk=row.get("Internal Hard Disk"),
            disk_type=row.get("Disk Type"),
            qty=row.get("Qty"),
            raid=row.get("Raid"),
            ram=row.get("Ram"),
            network_card=row.get("Network Card"),
            hba_card=row.get("HBA Card"),
            location=row.get("Location"),
            os_version=row.get("OS Version"),
            ip_address=row.get("IP address"),
            subnet_mask=row.get("Subnet Mask"),
            purchase_date=_parse_date(row.get("Purchase Date")),
        ))
    return assets

def _process_switches(df):
    """Process switches rows"""
    assets = []
    for _, row in df.iterrows():
        assets.append(Asset(
            company_name=row.get("Company Name"),
            device_type="Switch",
            model=row.get("Model"),
            make=row.get("MAKE"),
            serial_number=row.get("Serial No."),
            no_of_ports=row.get("No. of Ports"),
            os_version=row.get("OS Version"),
            ip_address=row.get("IP address"),
            subnet_mask=row.get("Subnet Mask"),
            purchase_date=_parse_date(row.get("Purchase Date")),
            additional_device=row.get("Additional Device"),
            remarks=row.get("Remarks","")
        ))
    return assets

def _process_storage(df):
    """Process storage rows"""
    assets = []
    for _, row in df.iterrows():
        assets.append(Asset(
            company_name=row.get("Company Name"),
            device_type="Storage",
            model=row.get("Model"),
            make=row.get("MAKE"),
            serial_number=row.get("Serial No."),
            total_capacity=row.get("Total Capacity"),
            disk_type=row.get("Disk Type"),
            os_version=row.get("OS Version"),
            ip_address=row.get("IP address"),
            subnet_mask=row.get("Subnet Mask"),
            purchase_date=_parse_date(row.get("Purchase Date")),
            additional_device=row.get("Additional Device"),
            remarks=row.get("Remarks","")
        ))
    return assets

def _parse_date(date_str):
    """Parse date string to datetime object, returns None if invalid."""
    if pd.isna(date_str):
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(date_str), fmt)
        except Exception:
            continue
    return None  # Only return None if all formats fail