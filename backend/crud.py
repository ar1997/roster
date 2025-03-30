from sqlalchemy.orm import Session
from models import Shift
from schemas import ShiftCreate

def get_shifts(db: Session):
    return db.query(Shift).all()

def create_shift(db: Session, shift: ShiftCreate):
    db_shift = Shift(**shift.dict())
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift

def delete_shift(db: Session, shift_id: int):
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if shift:
        db.delete(shift)
        db.commit()
        return {"message": "Deleted"}
    return {"message": "Shift not found"}
