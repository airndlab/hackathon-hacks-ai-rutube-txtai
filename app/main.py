from fastapi import FastAPI, Request

from app import index

app = FastAPI()


@app.get("/")
async def status():
    return {"status": "UP"}


@app.post("/search")
async def search(request: Request):
    json = await request.json()
    query = json['query']
    size = json['size']
    return {
        "results": index.search_videos(query, size),
        "channels": index.search_channels(query, size)
    }


@app.get("/suggests/{query}")
async def suggests(query: str, max_cost: int, size: int = 10):
    return list(map(lambda suggest: {"title": suggest}, index.search_suggests(query, max_cost, size)))
