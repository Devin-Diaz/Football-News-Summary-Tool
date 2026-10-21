from fastapi import APIRouter

from app.schemas import Article
from football_news.service import get_completed_news_summaries, run_news_pipeline

HTTP_200_OK = 200
HTTP_404_NOT_FOUND = 404

router = APIRouter(
    prefix="/v1",
    tags=["Articles"],
)

# Fetch completed entries
@router.get(
    "/articles",
    status_code=HTTP_200_OK,
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


# Generate new entries
@router.post(
    "/refresh_news",
    status_code=HTTP_200_OK,
    response_model=str,
    summary="Refresh flow for new football articles",
    description=(
        "Invokes refresh workflow that will generate a new set of "
        "summarized articles. Does not return articles, only creation."
    ),
)
def refresh_articles():
    run_news_pipeline()