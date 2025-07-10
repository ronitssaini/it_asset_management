from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.services.excel_handler import clean_and_parse_inventory
from backend.dependencies import get_db
import tempfile
import os
from backend.models.asset import Asset


router = APIRouter(prefix="/upload", tags=["upload"])

def asset_to_dict(asset):
    return {c.name: getattr(asset, c.name) for c in asset.__table__.columns}

@router.post("/excel")
async def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(400, detail="Only Excel files are accepted")
    
    try:
        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Process Excel (clean and parse)
        assets = clean_and_parse_inventory(tmp_path)
        print(f"[DEBUG] Parsed {len(assets)} assets from Excel:")
        for asset in assets:
            print(asset)
        
        # Filter out assets with duplicate serial_number by querying DB for each
        new_assets = []
        skipped = 0
        for asset in assets:
            exists = db.query(Asset).filter_by(serial_number=asset.serial_number).first()
            if exists:
                print(f"[DEBUG] Skipping duplicate asset with serial_number: {asset.serial_number}")
                skipped += 1
            else:
                new_assets.append(asset)
        print(f"[DEBUG] Skipping {skipped} duplicate assets. Inserting {len(new_assets)} new assets.")
        
        # Save to database
        try:
            db.add_all(new_assets)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"[ERROR] Database error: {e}")
            raise HTTPException(500, detail=f"Database error: {str(e)}")
        
        # Cleanup
        os.unlink(tmp_path)
        
        return JSONResponse({
            "filename": file.filename,
            "parsed_items": len(assets),
            "inserted_items": len(new_assets),
            "skipped_duplicates": skipped,
            "sample_item": asset_to_dict(new_assets[0]) if new_assets else None
        })
    except Exception as e:
        print(f"[ERROR] Processing failed: {e}")
        raise HTTPException(500, detail=f"Processing failed: {str(e)}")