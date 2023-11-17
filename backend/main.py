
# from fastapi import FastAPI, HTTPException, Depends, status
# from httpx import AsyncClient
# from sqlalchemy.orm import Session

# from database import SessionLocal, engine, Player, RatingHistory
# app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# async def get_bearer_token():
#     # Implement your logic to get the Bearer token, e.g., from a database, environment variable, etc.
#     return "lip_eecIEsURMcMv7mXFXEsv"


# async def fetch_rating_history(username: str, bearer_token: str = Depends(get_bearer_token)):
#     headers = {"Authorization": f"Bearer {bearer_token}"}

#     url = f"https://lichess.org/api/user/{username}/rating-history"

#     async with AsyncClient() as client:
#         try:
#             response = await client.get(url, headers=headers)
#             response.raise_for_status()  # Raise an HTTPError for bad responses
#             data = response.json()
#             return data
#         except HTTPException as e:
#             raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")


# @app.get("/player/{username}")
# async def rating_history(username: str):
#     return await fetch_rating_history(username)

# @app.get("/top-players")
# async def top_players(bearer_token: str = Depends(get_bearer_token)):
#     headers = {"Authorization": f"Bearer {bearer_token}"}
#     url = f"https://lichess.org/api/player"
#     async with AsyncClient() as client:
#         try:
#             response = await client.get(url, headers=headers)
#             response.raise_for_status()  # Raise an HTTPError for bad responses
#             data = response.json()
#             return data
#         except HTTPException as e:
#             raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")


# @app.post("/create-player/{username}")
# async def create_player(username: str, db: Session = Depends(get_db)):
#     player_history = await fetch_rating_history(username)

#     if player_history:
#         db_player = Player(username=username)
#         rating_history = RatingHistory(rating=player_history)
#         db_player.rating_history.append(rating_history)

#         db.add(db_player)
#         db.commit()
#         db.refresh(db_player)
#         return db_player

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player history not found")

# @app.get("/player/{username}/rating-history")
# def get_player_rating_history(username: str, db: Session  = Depends(get_db)):
#     # Step 1: Query the database to get the player by username
#     player = db.query(Player).filter(Player.username == username).first()

#     # Step 2: Access the rating_history attribute of the player instance
#     if player:
#         # Extract relevant information from the rating history
#         rating_history = [
#             {
#                 "username": player.username,
#                 "timestamp": entry.timestamp,
#                 "rating": entry.rating
#             }
#             for entry in player.rating_history
#         ]
#         return rating_history




# main.py

from fastapi import FastAPI, HTTPException, Request,Header,Depends, status
from api import players, top_players, rating_history,store_player_with_rating
from auth_api  import login,signin
from jose import JWTError, jwt
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

# OAuth2PasswordBearer instance for Bearer authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decoding and verifying the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise credentials_exception

    return username

# Custom middleware to check authentication header
async def auth_middleware(request: Request, call_next):
    auth_header = request.headers.get("Authorization")
    print(auth_header)
    if not auth_header or "Bearer" not in auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # If authentication is successful, proceed to the next middleware or the route handler
    response = await call_next(request)
    return response



origins = [
    "http://localhost",
    "http://localhost:3000", 
    "http://localhost:5173"
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
        allow_origins=origins,
         allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(login.router)
app.include_router(signin.router)
app.include_router(players.router, dependencies=[Depends(get_current_user)])
app.include_router(rating_history.router, dependencies=[Depends(get_current_user)])