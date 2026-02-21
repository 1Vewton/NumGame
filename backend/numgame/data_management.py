from numgame.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime

async def register():
    # Database Connection
    engine = create_async_engine(settings.database_url, echo=True)
    DBSession = sessionmaker(engine, class_=AsyncSession)
    # Get time
    date_time = datetime.now()
