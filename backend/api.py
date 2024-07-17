from fastapi import FastAPI
from pydantic import BaseModel


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


class SearchResponse(BaseModel):
    quotes: list[Quote]
    tags: list[Tag]


app = FastAPI()


@app.post('/api/search')
async def search(req: SearchRequest) -> SearchResponse:
    return SearchResponse(quotes=[
    ], tags=[
    ])
