from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"

ARTICLE_METADATA_PATH = DATA_DIR / "article_data.json"
DATABASE_PATH = DATABASE_DIR / "football_news.db"


def create_directories():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

