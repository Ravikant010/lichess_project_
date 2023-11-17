from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

# Set up a password context for hashing and verification
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify a password
def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

router = APIRouter()


class Req(BaseModel):
    username: str
    password: str 




@router.post("/login")
async def login( user_data: Req, db: Session = Depends(get_db)):
    username = user_data.username
    password = user_data.password
    # Check if the username exists
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Generate an access token
    access_token = create_access_token({"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
