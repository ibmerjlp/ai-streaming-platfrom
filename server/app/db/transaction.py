from contextlib import asynccontextmanager

@asynccontextmanager
async def transaction(session):
    try:
        await session.execute("BEGIN")
        yield
        await session.commit()
    except Exception:
        await session.rollback()
        raise