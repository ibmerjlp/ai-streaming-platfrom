import asyncio
import subprocess
from app.db.init_db import init_db

async def main():
    print("Hello from server!")

    await init_db()
    subprocess.run(
        ["uvicorn", "app.main:app", "--reload"],
        check=True
    )


if __name__ == "__main__":
    asyncio.run(main())
