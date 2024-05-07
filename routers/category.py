from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models import Category
from pydantic import BaseModel


router = APIRouter(prefix="/categories", tags=["categories"])



class CategoryRead(BaseModel):
    category_id: int
    category_name: str

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CategoryRead])
async def read_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories
