import sqlite3
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router
from football_news.config import BASE_DIR, DATABASE_PATH, create_directories
from football_news.db_operations import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv(BASE_DIR / ".env")
    create_directories()

    conn = sqlite3.connect(DATABASE_PATH)

    try:
        conn.execute("PRAGMA foreign_keys = ON")
        create_tables(conn)
    finally:
        conn.close()

    yield


app = FastAPI(
    title="Football News Summary API",
    description=(
        "AI-generated summaries of football reporting across "
        "Europe's major leagues and the UEFA Champions League."
    ),
    version="0.1.0",
    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "Articles",
            "description": "",
        },
        {
            "name": "Health",
            "description": "Check whether the API is running.",
        },
    ],
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.include_router(router)

app.mount(
    "/ui",
    StaticFiles(directory=BASE_DIR / "football_news_ui", html=True),
    name="football_news_ui",
)

@app.get("/health", tags=["Health"], summary="Check API availability")
def health_check():
    return {"status": "ok"}