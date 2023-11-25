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
async def root(search_request: SearchRequest):
    return {
        "results": index.search_videos(search_request.query, search_request.size),
        "channels": index.search_channels(search_request.query, search_request.size)
    }
