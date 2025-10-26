from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from deps import get_db
from schemas import UserCreate, Token
from crud import create_user, authenticate, get_user_by_email
from auth_utils import create_access_token
from tasks import send_welcome_email
from messaging import publish_user_created

router = APIRouter()

@router.post("/register", response_model=dict)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = create_user(db, payload.email, payload.password)
    # Lanza tarea en background (Celery)
    send_welcome_email.delay(user.email)
    # Publica evento en RabbitMQ (tolerante a fallos)
    publish_user_created(user.email)
    return {"id": user.id, "email": user.email}

@router.post("/token", response_model=Token)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access = create_access_token(subject=user.email)
    return {"access_token": access, "token_type": "bearer"}
