from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
# Update the connection string with correct credentials


engine = create_engine(os.environ.get("SQLALCHEMY_DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

    # Define a one-to-many relationship with RatingHistory
    rating_history = relationship("RatingHistory", back_populates="player")

class RatingHistory(Base):
    __tablename__ = "rating_history"
    
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(JSONB)

    # Use server_default to set the default timestamp on the database side
    timestamp = Column(DateTime, server_default=func.now())

    # Set up a foreign key relationship
    player_id = Column(Integer, ForeignKey("players.id"))
    
    # Define a many-to-one relationship with Player
    player = relationship("Player", back_populates="rating_history")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True,  index = True)
    username = Column(String, unique = True, index = True)
    password = Column(String)


# Create the tables in the database
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
