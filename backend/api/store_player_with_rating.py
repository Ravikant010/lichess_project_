from database import get_db, Player, RatingHistory
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
# from fetch_rating_history import fetch_rating_history
from api.fetch_rating_history import fetch_rating_history

router = APIRouter()

@router.post("/create-player/{username}")
async def create_player(username: str, db: Session = Depends(get_db)):
    player_history = await fetch_rating_history(username)
    if player_history:
        db_player = Player(username=username)
        rating_history = RatingHistory(rating=player_history)
        db_player.rating_history.append(rating_history)
        db.add(db_player)
        db.commit()
        db.refresh(db_player)
        return db_player
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player history not found")