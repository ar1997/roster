# backend/main.py
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import crud
import export_import
from schemas import ShiftCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/shifts")
def get_shifts(db: Session = Depends(get_db)):
    return crud.get_shifts(db)

@app.post("/shifts")
def create_shift(shift: ShiftCreate, db: Session = Depends(get_db)):
    return crud.create_shift(db, shift)

@app.delete("/shifts/{shift_id}")
def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    return crud.delete_shift(db, shift_id)

@app.post("/export")
def export_data():
    path = export_import.export_to_zip()
    return FileResponse(path, media_type='application/zip', filename="roster_export.zip")

@app.post("/import")
def import_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return export_import.import_from_zip(file.file, db)

