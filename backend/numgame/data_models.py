from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

# Base
Base = declarative_base()

# Games data
class Games(Base):
    # Table name
    __tablename__ = 'Games'
    # Columns
    id = Column(String(100), primary_key=True)
    first_move = Column(String(100), ForeignKey("Players.id"),nullable=False)
    second_move = Column(String(100), ForeignKey("Players.id"), nullable=False)
    winner = Column(String(100), ForeignKey("Players.id"), nullable=True)
    rounds = Column(Integer, nullable=False)
    started_time = Column(DateTime, nullable=False)
    # constraints
    __table_args__ = (
        CheckConstraint('first_move != second_move', name='check_players_different'),
    )
    # Relations
    first_player = relationship("Players", foreign_keys=[first_move])
    second_player = relationship("Players", foreign_keys=[second_move])
    winner_player = relationship("Players", foreign_keys=[winner])

# Player data
class Players(Base):
    # Table name
    __tablename__ = "Players"
    # Columns
    id = Column(String(100), primary_key=True)
    user_name = Column(String(100), unique=True, nullable=False)
    registered_at = Column(DateTime, nullable=False)
    wins = Column(Integer, nullable=False)
    total_games = Column(Integer, nullable=False)
    # to dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "registered_at": self.registered_at,
            "wins": self.wins,
            "total_games": self.total_games
        }