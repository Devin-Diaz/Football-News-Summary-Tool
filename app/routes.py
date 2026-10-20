from fastapi import APIRouter

from app.schemas import Article
from football_news.service import get_completed_news_summaries

router = APIRouter(
    prefix="/articles",
    tags=["Articles"],
)


@router.get(
    "",
    response_model=list[Article],
    summary="Get summarized football news",
    description=(
        "Returns completed article summaries with their original "
        "headlines, publishers, publication dates, and source links. "
        "Reads saved results without triggering retrieval or LLM calls."
    ),
)
def list_articles():
    return get_completed_news_summaries()