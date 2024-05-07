from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import SessionLocal
from models import TermsAndCondition

router = APIRouter(prefix="/terms", tags=["terms"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TermsBase(BaseModel):
    title: str
    content: str

class TermsCreate(TermsBase):
    pass

class TermsRead(TermsBase):
    terms_id: int
    registration_datetime: str
    registrant: str

    class Config:
        orm_mode = True

# 약관 생성 API
@router.post("/", response_model=TermsRead, status_code=201)
async def create_terms(terms_data: TermsCreate, db: Session = Depends(get_db)):
    new_terms = TermsAndCondition(**terms_data.dict())
    db.add(new_terms)
    db.commit()
    db.refresh(new_terms)
    return new_terms

# 모든 약관 조회 API
@router.get("/", response_model=List[TermsRead])
async def read_terms(db: Session = Depends(get_db)):
    terms_list = db.query(TermsAndCondition).all()
    return terms_list

# 특정 약관 조회 API
@router.get("/{terms_id}", response_model=TermsRead)
async def read_term(terms_id: int, db: Session = Depends(get_db)):
    term = db.query(TermsAndCondition).filter(TermsAndCondition.terms_id == terms_id).first()
    if term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return term

# 약관 수정 API
@router.put("/{terms_id}", response_model=TermsRead)
async def update_term(terms_id: int, terms_data: TermsBase, db: Session = Depends(get_db)):
    term = db.query(TermsAndCondition).filter(TermsAndCondition.terms_id == terms_id).first()
    if term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    for var, value in vars(terms_data).items():
        setattr(term, var, value)
    db.commit()
    return term

# 약관 삭제 API
@router.delete("/{terms_id}", status_code=204)
async def delete_term(terms_id: int, db: Session = Depends(get_db)):
    term = db.query(TermsAndCondition).filter(TermsAndCondition.terms_id == terms_id).first()
    if term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    db.delete(term)
    db.commit()
    return {"detail": "Term deleted successfully"}
