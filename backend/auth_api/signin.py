from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db,User
import bcrypt
from pydantic import BaseModel
def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

class Req(BaseModel):
    username: str
    password: str 


router = APIRouter()



@router.post("/signup")
async def signup(user_data: Req, db: Session = Depends(get_db)):
    # Extract username and password from the request body

    print(user_data)
    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    # Hash the password before storing it
    hashed_password = get_password_hash(user_data.password)

    # Create a new user in the database
    new_user = User(username=user_data.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User successfully registered"}