from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Category
from pydantic import BaseModel

router = APIRouter(prefix="/categories", tags=["categories"])


class CategoryRead(BaseModel):
    category_id: int
    category_name: str
    guidelines: str

    class Config:
        orm_mode = True


@router.get("/", response_model=List[CategoryRead])
async def read_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    for category in categories:
        if category.guidelines is None:
            category.guidelines = ""
    return categories


@router.get("/{category_id}", response_model=CategoryRead)
async def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.guidelines is None:
        category.guidelines = ""
    return category
