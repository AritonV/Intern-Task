from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from ..auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token
from ..database import get_session
from ..models import User

router = APIRouter()


@router.post("/register", response_model=dict, tags=["auth"])
def register_user(user: User, session: Session = Depends(get_session)):
  existing_user = session.exec(
    select(User).where(User.email == user.email)).first()
  if existing_user:
    raise HTTPException(status_code=400, detail="Email already registered")

  session.add(user)
  session.commit()
  session.refresh(user)
  return {"message": "User registered successfully"}


@router.post("/token", tags=["auth"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
  user = authenticate_user(session, form_data.username, form_data.password)
  if not user:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
      data={"sub": user.email}, expires_delta=access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}
