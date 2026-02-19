from numgame.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database Connection
engine = create_engine(settings.database_url)
DBSession = sessionmaker(bind=engine)