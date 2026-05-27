from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "db" / "db.sqlite3"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"