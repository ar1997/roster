# backend/export_import.py
import json, zipfile, os
from io import BytesIO
from models import Shift
from sqlalchemy.orm import Session
from datetime import datetime
import tempfile

def export_to_zip():
    from database import SessionLocal
    db = SessionLocal()
    shifts = db.query(Shift).all()
    shift_data = [
        {
            "id": s.id,
            "employee_name": s.employee_name,
            "date": s.date.isoformat(),
            "start_time": s.start_time.isoformat(),
            "end_time": s.end_time.isoformat()
        }
        for s in shifts
    ]
    
    temp_dir = tempfile.mkdtemp()
    json_path = os.path.join(temp_dir, "shifts.json")
    with open(json_path, "w") as f:
        json.dump(shift_data, f)

    zip_path = os.path.join(temp_dir, "export.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(json_path, arcname="shifts.json")

    return zip_path

def import_from_zip(file, db: Session):
    with zipfile.ZipFile(file) as zipf:
        if "shifts.json" not in zipf.namelist():
            return {"error": "shifts.json not found in zip"}
        with zipf.open("shifts.json") as f:
            shift_data = json.load(f)
            for s in shift_data:
                shift = Shift(
                    employee_name=s["employee_name"],
                    date=datetime.fromisoformat(s["date"]).date(),
                    start_time=datetime.fromisoformat(s["start_time"]).time(),
                    end_time=datetime.fromisoformat(s["end_time"]).time(),
                )
                db.add(shift)
            db.commit()
    return {"message": "Import successful"}

