from pathlib import Path
from football_news.service import run_news_pipeline

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "database"

def main():
    result = run_news_pipeline()
    print(result)

if __name__ == "__main__":
    main()