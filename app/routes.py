from fastapi import APIRouter

from typing import Annotated, Literal
from fastapi import Query
from app.schemas import ArticlePage
from fastapi import HTTPException
from app.schemas import Article
from football_news.service import (get_completed_news_summaries, 
                                   run_news_pipeline,
                                   get_article_by_id)

HTTP_200_OK = 200
HTTP_404_NOT_FOUND = 404

Competition = Literal[
    "UEFA Champions League",
    "Premier League",
    "La Liga",
    "Serie A",
    "Bundesliga",
    "Ligue 1",
]


router = APIRouter(
    prefix="/v1/articles",
    tags=["Articles"],
)


# Fetch completed entries
# @router.get(
#     "/all",
#     status_code=HTTP_200_OK,
#     response_model=list[Article],
#     summary="Get summarized football news",
#     description=(
#         "Returns completed article summaries with their original "
#         "headlines, publishers, publication dates, and source links. "
#         "Reads saved results without triggering retrieval or LLM calls."
#     ),
# )
# def list_articles():
#     return get_completed_news_summaries()


# Fetch completed entries
@router.get(
    "/all",
    response_model=ArticlePage,
    summary="Get football summaries",
)
def list_articles(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=50)] = 10,
    competition: Competition | None = None,
):
    return get_completed_news_summaries(
        page=page,
        page_size=page_size,
        competition=competition,
    )


# Fetch a single article by ID
@router.get(
    "/{article_id}",
    summary='Retrieve article by id',
    response_model=Article,
)
def retrieve_article_by_id(article_id: int):
    article = get_article_by_id(article_id)

    if article is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Article not found")

    return article


# Generate new entries
@router.post(
    "/refresh_news",
    status_code=HTTP_200_OK,
    response_model=dict[str, str],
    summary="Refresh flow for new football articles",
    description=(
        "Invokes refresh workflow that will generate a new set of "
        "summarized articles. Does not return articles, only creation."
    ),
)
def refresh_articles():
    return run_news_pipeline()
