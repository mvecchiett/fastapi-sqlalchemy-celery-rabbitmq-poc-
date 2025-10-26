from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from deps import get_db, get_current_user
from schemas import UserOut

router = APIRouter()

@router.get("/me", response_model=UserOut)
def me(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return current_user
