from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import Annotated
# user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from models import Users
from routers.auth import get_current_user, get_db, oauth2_bearer, SECRETE_KEY, ALGORITHM
# schemas.py
from pydantic import BaseModel

class UserRead(BaseModel):
    username: str
    email: str
    phone_number: str
    gender: str
    school: str

    class Config:
        orm_mode = True

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/me")
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get('id')
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'JWT Error: {str(e)}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {str(e)}')

