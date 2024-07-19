from fastapi import FastAPI
from pydantic import BaseModel
from search import search_quotes


class Quote(BaseModel):
    id: str
    quote: str
    author: str
    tags: list[str]
    score: float


class Tag(BaseModel):
    tag: str
    count: int


class SearchRequest(BaseModel):
    query: str
    filters: list[str]
    knn: bool
    start: int


class SearchResponse(BaseModel):
    quotes: list[Quote]
    tags: list[Tag]
    start: int
    total: int


app = FastAPI()


@app.post('/api/search')
async def search(req: SearchRequest) -> SearchResponse:
    quotes, tags, total = await search_quotes(req.query, req.filters, use_knn=req.knn, start=req.start)
    return SearchResponse(quotes=[
        Quote(id=q.meta.id, quote=q.quote, author=q.author, tags=q.tags, score=q.meta.score)
        for q in quotes
    ], tags=[
        Tag(tag=t[0], count=t[1]) for t in tags
    ], start=req.start, total=total)
