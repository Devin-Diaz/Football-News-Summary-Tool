from pydantic import BaseModel


# Article data presented to user
class Article(BaseModel):
    id: int
    title: str
    published_at: str | None
    publisher: str | None
    publisher_url: str | None
    summary: str


# Response for Pagination metadata
class ArticlePage(BaseModel):
    items: list[Article]
    page: int
    page_size: int
    total: int
    total_pages: int


# Complete article record as it's stored in database
class ArticleRecord(BaseModel):
    id: int
    source_url: str
    title: str
    published_at: str | None
    publisher: str | None
    publisher_url: str | None
    description: str | None
    full_text: str | None
    summary: str | None