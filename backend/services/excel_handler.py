import pandas as pd
from datetime import datetime
from backend.models.asset import Asset

desktop_columns = [
    "Company Name", "Device Type", "MAKE", "Serial No.", "Processor", "Hard disk", "Ram", "Monitor", "Location",
    "OS Version", "IP address", "Subnet Mask", "Purchase Date", "Additional Device", "Emp. Code", "Name", "Function", "Role", "Remarks"
]
# Add laptops_columns as same as desktop_columns
laptops_columns = desktop_columns.copy()
server_columns = [
    "Company Name", "Typer", "MAKE", "Serial No.", "Processor Typer", "Processor", "Total Processo Core", "Internal Hard Disk",
    "Disk Type", "Qty", "Raid", "Ram", "Network Card", "HBA Card", "Location", "OS Version", "IP address", "Subnet Mask", "Purchase Date"
]
switch_columns = [
    "Company Name", "Model", "MAKE", "Serial No.", "No. of Ports", "OS Version", "IP address", "Subnet Mask", "Purchase Date", "Additional Device", "Remarks"
]
storage_columns = [
    "Company Name", "Device Type", "Model", "MAKE", "Serial No.", "Total Capacity", "Disk type", "OS Version", "IP address", "Subnet Mask", "Purchase Date", "Additional Device", "Remarks"
]

required_columns = {
    "Desktop": ["Serial No.", "Company Name", "Device Type"],
    "Laptop": ["Serial No.", "Company Name", "Device Type"],
    "Server": ["Serial No.", "Company Name"],
    "Switches": ["Serial No.", "Company Name"],
    "Storage": ["Serial No.", "Company Name", "Device Type"]
}

sheet_columns = {
    "Desktop": desktop_columns,
    "Laptop": laptops_columns,
    "Server": server_columns,
    "Switches": switch_columns,
    "Storage": storage_columns
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
    for sheet in ["Desktop", "Laptop", "Server", "Switches", "Storage"]:
        if sheet in xls.sheet_names:
            print(f"[DEBUG] Cleaning and parsing sheet: {sheet}")
            df = pd.read_excel(xls, sheet_name=sheet, skiprows=1)
            cleaned_df = clean_sheet(df, sheet)
            print(f"[DEBUG] {sheet}: {len(cleaned_df)} rows after cleaning.")
            if sheet in ["Desktop", "Laptop"]:
                assets.extend(_process_computers(cleaned_df))
            elif sheet == "Server":
                assets.extend(_process_servers(cleaned_df))
            elif sheet == "Switches":
                assets.extend(_process_switches(cleaned_df))
            elif sheet == "Storage":
                assets.extend(_process_storage(cleaned_df))
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
            device_type=row.get("Device Type", "Storage"),
            model=row.get("Model"),
            make=row.get("MAKE"),
            serial_number=row.get("Serial No."),
            total_capacity=row.get("Total Capacity"),
            disk_type=row.get("Disk type"),
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

def clean_and_parse_csv_inventory(file_path: str):
    """Clean and parse CSV inventory file for backend upload."""
    try:
        # Try to detect the delimiter
        df = pd.read_csv(file_path, nrows=1)
        delimiter = ','
        
        # Read the full CSV file
        df = pd.read_csv(file_path, delimiter=delimiter)
        
        # Determine device type from column names or data
        device_type = _detect_device_type_from_csv(df)
        
        print(f"[DEBUG] Detected device type: {device_type}")
        print(f"[DEBUG] CSV columns: {list(df.columns)}")
        
        # Clean the dataframe
        df = df.rename(columns=lambda x: x.strip() if isinstance(x, str) else x)
        
        # Map CSV columns to expected columns based on device type
        if device_type in ["Desktop", "Laptop"]:
            df = _map_csv_to_computer_columns(df)
            return _process_computers(df)
        elif device_type == "Server":
            df = _map_csv_to_server_columns(df)
            return _process_servers(df)
        elif device_type == "Switch":
            df = _map_csv_to_switch_columns(df)
            return _process_switches(df)
        elif device_type == "Storage":
            df = _map_csv_to_storage_columns(df)
            return _process_storage(df)
        else:
            # Default to computer processing
            df = _map_csv_to_computer_columns(df)
            return _process_computers(df)
            
    except Exception as e:
        print(f"[ERROR] CSV processing failed: {e}")
        raise e

def _detect_device_type_from_csv(df):
    """Detect device type from CSV column names or data."""
    columns = [col.lower() for col in df.columns]
    
    # Check for device type column
    if 'device type' in columns:
        device_types = df['Device Type'].dropna().unique()
        if len(device_types) > 0:
            return str(device_types[0]).strip()
    
    # Check for specific columns that indicate device type
    if any(col in columns for col in ['no. of ports', 'number of ports']):
        return "Switch"
    elif any(col in columns for col in ['total capacity', 'disk type']):
        return "Storage"
    elif any(col in columns for col in ['processor type', 'total processo core', 'raid']):
        return "Server"
    elif any(col in columns for col in ['hard disk', 'ram', 'monitor']):
        return "Desktop"  # Default to Desktop for computers
    
    return "Desktop"  # Default fallback

def _map_csv_to_computer_columns(df):
    """Map CSV columns to computer (Desktop/Laptop) expected columns."""
    column_mapping = {
        'Company Name': 'Company Name',
        'Device Type': 'Device Type',
        'MAKE': 'MAKE',
        'Serial No.': 'Serial No.',
        'Serial Number': 'Serial No.',
        'Processor': 'Processor',
        'Hard disk': 'Hard disk',
        'Hard Disk': 'Hard disk',
        'Ram': 'Ram',
        'RAM': 'Ram',
        'Monitor': 'Monitor',
        'Location': 'Location',
        'OS Version': 'OS Version',
        'OS': 'OS Version',
        'IP address': 'IP address',
        'IP': 'IP address',
        'Subnet Mask': 'Subnet Mask',
        'Purchase Date': 'Purchase Date',
        'Additional Device': 'Additional Device',
        'Emp. Code': 'Emp. Code',
        'Employee Code': 'Emp. Code',
        'Name': 'Name',
        'Employee Name': 'Name',
        'Function': 'Function',
        'Role': 'Role',
        'Remarks': 'Remarks'
    }
    
    # Rename columns based on mapping
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})
    
    # Add missing columns with None values
    expected_columns = desktop_columns
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    
    # Filter to only expected columns
    df = df[[col for col in expected_columns if col in df.columns]]
    
    # Drop rows with missing required columns
    req = required_columns["Desktop"]
    df = df.dropna(subset=[col for col in req if col in df.columns])
    df = df.drop_duplicates(subset=["Serial No."])
    
    return df

def _map_csv_to_server_columns(df):
    """Map CSV columns to server expected columns."""
    column_mapping = {
        'Company Name': 'Company Name',
        'Typer': 'Typer',
        'Type': 'Typer',
        'MAKE': 'MAKE',
        'Serial No.': 'Serial No.',
        'Serial Number': 'Serial No.',
        'Processor Typer': 'Processor Typer',
        'Processor Type': 'Processor Typer',
        'Processor': 'Processor',
        'Total Processo Core': 'Total Processo Core',
        'Total Processor Core': 'Total Processo Core',
        'Internal Hard Disk': 'Internal Hard Disk',
        'Disk Type': 'Disk Type',
        'Qty': 'Qty',
        'Quantity': 'Qty',
        'Raid': 'Raid',
        'RAID': 'Raid',
        'Ram': 'Ram',
        'RAM': 'Ram',
        'Network Card': 'Network Card',
        'HBA Card': 'HBA Card',
        'Location': 'Location',
        'OS Version': 'OS Version',
        'OS': 'OS Version',
        'IP address': 'IP address',
        'IP': 'IP address',
        'Subnet Mask': 'Subnet Mask',
        'Purchase Date': 'Purchase Date'
    }
    
    # Rename columns based on mapping
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})
    
    # Add missing columns with None values
    expected_columns = server_columns
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    
    # Filter to only expected columns
    df = df[[col for col in expected_columns if col in df.columns]]
    
    # Drop rows with missing required columns
    req = required_columns["Server"]
    df = df.dropna(subset=[col for col in req if col in df.columns])
    df = df.drop_duplicates(subset=["Serial No."])
    
    return df

def _map_csv_to_switch_columns(df):
    """Map CSV columns to switch expected columns."""
    column_mapping = {
        'Company Name': 'Company Name',
        'Model': 'Model',
        'MAKE': 'MAKE',
        'Serial No.': 'Serial No.',
        'Serial Number': 'Serial No.',
        'No. of Ports': 'No. of Ports',
        'Number of Ports': 'No. of Ports',
        'OS Version': 'OS Version',
        'OS': 'OS Version',
        'IP address': 'IP address',
        'IP': 'IP address',
        'Subnet Mask': 'Subnet Mask',
        'Purchase Date': 'Purchase Date',
        'Additional Device': 'Additional Device',
        'Remarks': 'Remarks'
    }
    
    # Rename columns based on mapping
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})
    
    # Add missing columns with None values
    expected_columns = switch_columns
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    
    # Filter to only expected columns
    df = df[[col for col in expected_columns if col in df.columns]]
    
    # Drop rows with missing required columns
    req = required_columns["Switches"]
    df = df.dropna(subset=[col for col in req if col in df.columns])
    df = df.drop_duplicates(subset=["Serial No."])
    
    return df

def _map_csv_to_storage_columns(df):
    """Map CSV columns to storage expected columns."""
    column_mapping = {
        'Company Name': 'Company Name',
        'Device Type': 'Device Type',
        'Model': 'Model',
        'MAKE': 'MAKE',
        'Serial No.': 'Serial No.',
        'Serial Number': 'Serial No.',
        'Total Capacity': 'Total Capacity',
        'Disk type': 'Disk type',
        'Disk Type': 'Disk type',
        'OS Version': 'OS Version',
        'OS': 'OS Version',
        'IP address': 'IP address',
        'IP': 'IP address',
        'Subnet Mask': 'Subnet Mask',
        'Purchase Date': 'Purchase Date',
        'Additional Device': 'Additional Device',
        'Remarks': 'Remarks'
    }
    
    # Rename columns based on mapping
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})
    
    # Add missing columns with None values
    expected_columns = storage_columns
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    
    # Filter to only expected columns
    df = df[[col for col in expected_columns if col in df.columns]]
    
    # Drop rows with missing required columns
    req = required_columns["Storage"]
    df = df.dropna(subset=[col for col in req if col in df.columns])
    df = df.drop_duplicates(subset=["Serial No."])
    
    return df