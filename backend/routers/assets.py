from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.auth.dependencies import admin_required, manager_or_admin_required
from backend.models.asset import Asset
from pydantic import BaseModel, validator, root_validator
from typing import List, Optional
from fastapi.responses import StreamingResponse
import csv
from datetime import date
from io import StringIO

# This is the critical line - must create the router instance
router = APIRouter(prefix="/assets", tags=["assets"])

# Pydantic schema for asset input/output
class AssetIn(BaseModel):
    company_name: str
    device_type: str
    serial_number: str
    location: str
    make: Optional[str] = None
    os_version: Optional[str] = None
    ip_address: Optional[str] = None
    subnet_mask: Optional[str] = None
    purchase_date: Optional[date] = None
    additional_device: Optional[str] = None
    remarks: Optional[str] = None
    employee_code: Optional[str] = None
    employee_name: Optional[str] = None
    function: Optional[str] = None
    role: Optional[str] = None
    typer: Optional[str] = None
    processor_type: Optional[str] = None
    processor: Optional[str] = None
    total_processor_core: Optional[int] = None
    internal_hard_disk: Optional[str] = None
    disk_type: Optional[str] = None
    qty: Optional[int] = None
    raid: Optional[str] = None
    ram: Optional[str] = None
    network_card: Optional[str] = None
    hba_card: Optional[str] = None
    model: Optional[str] = None
    no_of_ports: Optional[int] = None
    total_capacity: Optional[str] = None
    # New field for last 3 users
    last_users: Optional[list[str]] = None
    class Config:
        from_attributes = True

    @validator('purchase_date', pre=True)
    def parse_date(cls, v):
        if v is None or v == '':
            return None
        if isinstance(v, date):
            return v
        from datetime import datetime
        # Try DD-MM-YYYY
        try:
            return datetime.strptime(v, "%d-%m-%Y").date()
        except ValueError:
            pass
        # Try ISO
        try:
            return datetime.strptime(v, "%Y-%m-%d").date()
        except ValueError:
            pass
        raise ValueError("purchase_date must be in DD-MM-YYYY or YYYY-MM-DD format")

class AssetOut(AssetIn):
    class Config:
        from_attributes = True
        json_encoders = {date: lambda v: v.strftime('%d-%m-%Y') if v else '', list: lambda v: v if v else []}

    @validator(
        'company_name', 'device_type', 'serial_number', 'location', 'make', 'os_version', 'ip_address', 'subnet_mask',
        'additional_device', 'remarks', 'employee_code', 'employee_name', 'function', 'role', 'typer', 'processor_type',
        'processor', 'internal_hard_disk', 'disk_type', 'raid', 'ram', 'network_card', 'hba_card', 'model', 'total_capacity',
        pre=True, always=True
    )
    def none_to_empty_string(cls, v):
        return v if v is not None else ''

    @validator('last_users', pre=True, always=True)
    def parse_last_users(cls, v):
        import json
        if v is None or v == '' or v == '[]':
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
                return []
            except Exception:
                return []
        return []

    @root_validator(pre=True)
    def add_employee_name_to_last_users(cls, values):
        try:
            device_type = (values.get('device_type') or '').lower()
            if device_type not in ('desktop', 'laptop'):
                return values
            emp_name = values.get('employee_name') or ''
            if not emp_name:
                return values
            last_users = values.get('last_users') or []
            # ensure list
            if not isinstance(last_users, list):
                last_users = [last_users]
            # Prepend emp_name if not already present and not empty
            if emp_name and emp_name not in last_users:
                last_users = [emp_name] + last_users
            # Remove empty strings and keep unique
            last_users = [u for i, u in enumerate(last_users) if u and u not in last_users[:i]]
            values['last_users'] = last_users[:3]  # keep up to 3
            return values
        except Exception:
            return values


def asset_to_dict(asset):
    return {c.name: getattr(asset, c.name) for c in asset.__table__.columns}

@router.get("/", response_model=List[AssetOut])
def get_assets(db: Session = Depends(get_db), role: str = Depends(manager_or_admin_required)):
    assets = db.query(Asset).all()
    return assets

# In update_asset and create_asset, always sync employee_name and last_users for desktops/laptops
@router.put("/{serial_number}", response_model=AssetOut)
def update_asset(serial_number: str, asset: AssetIn, db: Session = Depends(get_db)):
    import json
    db_asset = db.query(Asset).filter_by(serial_number=serial_number).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    data = asset.dict()
    for k, v in data.items():
        if isinstance(v, str) and v.strip() == "":
            data[k] = None
    # Handle last_users for desktops and laptops only
    if asset.device_type in ["Desktop", "Laptop"]:
        last_users = asset.last_users or []
        if not isinstance(last_users, list):
            last_users = [last_users]
        # Always ensure employee_name is first
        emp_name = asset.employee_name or ""
        if emp_name and emp_name not in last_users:
            last_users = [emp_name] + last_users
        # Remove empty strings and keep unique
        last_users = [u for i, u in enumerate(last_users) if u and u not in last_users[:i]]
        last_users = last_users[:3]
        data["last_users"] = json.dumps(last_users)
    else:
        data["last_users"] = None
    for k, v in data.items():
        setattr(db_asset, k, v)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.post("/", response_model=AssetOut, status_code=status.HTTP_201_CREATED)
def create_asset(asset: AssetIn, db: Session = Depends(get_db)):
    import json
    if db.query(Asset).filter_by(serial_number=asset.serial_number).first():
        raise HTTPException(status_code=400, detail="Asset with this serial number already exists.")
    data = asset.dict()
    for k, v in data.items():
        if isinstance(v, str) and v.strip() == "":
            data[k] = None
    # Handle last_users for desktops and laptops only
    if asset.device_type in ["Desktop", "Laptop"]:
        last_users = asset.last_users or []
        if not isinstance(last_users, list):
            last_users = [last_users]
        # Always ensure employee_name is first
        emp_name = asset.employee_name or ""
        if emp_name and emp_name not in last_users:
            last_users = [emp_name] + last_users
        # Remove empty strings and keep unique
        last_users = [u for i, u in enumerate(last_users) if u and u not in last_users[:i]]
        last_users = last_users[:3]
        data["last_users"] = json.dumps(last_users)
    else:
        data["last_users"] = None
    db_asset = Asset(**data)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.delete("/{serial_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(serial_number: str, db: Session = Depends(get_db), role: str = Depends(admin_required)):
    asset = db.query(Asset).filter_by(serial_number=serial_number).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    db.delete(asset)
    db.commit()
    return

@router.get("/report")
def get_asset_report(
    type: Optional[str] = None,
    device_type: Optional[str] = None,
    location: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    role: str = Depends(manager_or_admin_required)
):
    query = db.query(Asset)
    if device_type:
        query = query.filter(Asset.device_type == device_type)
    if location:
        query = query.filter(Asset.location.ilike(f"%{location}%"))
    if start_date:
        query = query.filter(Asset.purchase_date >= start_date)
    if end_date:
        query = query.filter(Asset.purchase_date <= end_date)
    assets = query.all()
    # For type/location report, you could aggregate here if needed, but for now return all filtered assets
    return [asset_to_dict(a) for a in assets]

@router.get("/report/download")
def download_asset_report(
    type: Optional[str] = None,
    device_type: Optional[str] = None,
    location: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    role: str = Depends(manager_or_admin_required)
):
    query = db.query(Asset)
    if device_type:
        query = query.filter(Asset.device_type == device_type)
    if location:
        query = query.filter(Asset.location.ilike(f"%{location}%"))
    if start_date:
        query = query.filter(Asset.purchase_date >= start_date)
    if end_date:
        query = query.filter(Asset.purchase_date <= end_date)
    assets = query.all()
    output = StringIO()
    writer = csv.writer(output)
    if assets:
        writer.writerow([c.name for c in Asset.__table__.columns])
        for a in assets:
            writer.writerow([getattr(a, c.name) for c in Asset.__table__.columns])
    else:
        writer.writerow(["No data found for the selected filters."])
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=asset_report.csv"})