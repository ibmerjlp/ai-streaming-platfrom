import aiosqlite
from pathlib import Path
from app.core.config import DATABASE_PATH, SCHEMA_PATH

async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        with open (SCHEMA_PATH, "r") as f:
            await db.executescript(f.read())
        await db.commit()