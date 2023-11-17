from database import get_db, Player, RatingHistory
from fastapi import Depends, APIRouter,HTTPException,status
from sqlalchemy.orm import Session
from api.fetch_rating_history import fetch_rating_history
router = APIRouter()
@router.get("/player/{username}/rating-history")
async def get_player_rating_history(username: str, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.username == username).first()
    if player:
        rating_history = [
            {
                "username": player.username,
                "timestamp": entry.timestamp,
                "rating": entry.rating
            }
            for entry in player.rating_history
        ]
        return rating_history

    player_history = await fetch_rating_history(username)

    if player_history:
        db_player = Player(username=username)
        rating_history = RatingHistory(rating=player_history)
        db_player.rating_history.append(rating_history)
        db.add(db_player)
        db.add(rating_history)
        db.commit()
        db.refresh(db_player)
        return [
            {
                "username": db_player.username,
                "timestamp": entry.timestamp,
                "rating": entry.rating
            }
            for entry in db_player.rating_history
        ]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player history not found")