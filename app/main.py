from fastapi import FastAPI
from pydantic import BaseModel

from app import index

app = FastAPI()


@app.get("/")
async def status():
    return {"status": "UP"}


class SearchRequest(BaseModel):
    query: str
    size: int


@app.post("/search")
async def search(search_request: SearchRequest):
    return {
        "results": index.search_videos(search_request.query, search_request.size),
        "channels": index.search_channels(search_request.query, search_request.size)
    }


@app.get("/suggests/{query}")
async def suggests(query: str, max_cost: int, size: int = 10):
    return list(map(lambda suggest: {"title": suggest}, index.search_suggests(query, max_cost, size)))
