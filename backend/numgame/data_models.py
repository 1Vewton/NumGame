from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import inspect

# Base
class Base(DeclarativeBase):
    """Base class for SQLAlchemy models.

    All other models should inherit from this class.
    """

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
    # to dict
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

# Games data
class games(Base):
    # Table name
    __tablename__ = 'games'
    # Columns
    id = Column(String(100), primary_key=True)
    first_move = Column(String(100), ForeignKey("players.id", ondelete="CASCADE"),nullable=False)
    second_move = Column(String(100), ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    winner = Column(String(100), ForeignKey("players.id", ondelete="CASCADE"), nullable=True)
    rounds = Column(Integer, nullable=False)
    started_time = Column(DateTime, nullable=False)
    ended_time = Column(DateTime, nullable=True)
    # constraints
    __table_args__ = (
        CheckConstraint('first_move != second_move', name='check_players_different'),
    )
    # Relations
    first_player = relationship("players", foreign_keys=[first_move])
    second_player = relationship("players", foreign_keys=[second_move])
    winner_player = relationship("players", foreign_keys=[winner])
    # autogen repr
    def __repr__(self_):
        ret = f'{type(self_).__name__}<'
        for key in inspect(type(self_)).c.keys():
            ret += f'{key}: {getattr(self_, key)},'
        ret = ret.rstrip(',')
        ret += '>'
        return ret

# Player data
class players(Base):
    # Table name
    __tablename__ = "players"
    # Columns
    id = Column(String(100), primary_key=True)
    user_name = Column(String(100), unique=True, nullable=False)
    registered_at = Column(DateTime, nullable=False)
    wins = Column(Integer, nullable=False, default=0)
    total_games = Column(Integer, nullable=False, default=0)
    # autogen repr
    def __repr__(self_):
        ret = f'{type(self_).__name__}<'
        for key in inspect(type(self_)).c.keys():
            ret += f'{key}: {getattr(self_, key)},'
        ret = ret.rstrip(',')
        ret += '>'
        return ret