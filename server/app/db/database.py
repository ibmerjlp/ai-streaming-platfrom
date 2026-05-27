import aiosqlite
from app.core.config import DATABASE_PATH

async def get_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db