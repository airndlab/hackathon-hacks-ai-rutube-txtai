from fastapi import FastAPI
from pydantic import BaseModel

from app import index

app = FastAPI()


@app.get("/")
async def status():
    return {"status": "UP"}


class SearchRequest(BaseModel):
    query: str


@app.post("/search")
async def root(search_request: SearchRequest):
    return {"results": index.search(search_request.query)}
