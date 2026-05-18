from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "data" / "mini_erp.sqlite3"


def get_database_path():
    configured_path = os.getenv("MINI_ERP_DB_PATH")
    if configured_path:
        return Path(configured_path).expanduser().resolve()
    return DEFAULT_DATABASE_PATH
