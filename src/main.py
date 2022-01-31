from fastapi import FastAPI
from mangum import Mangum
from redis import Redis

from api_v1.api import router as api_router

app = FastAPI(
    title="My Awesome FastAPI app",
    description="This is super fancy, with auto docs and everything!",
    version="0.1.0",
)


@app.get("/redis", name="Redis", tags=["Redis"])
async def redis_check():
    try:
        redis = Redis(
            host="redis-test-2.kthrlr.ng.0001.use1.cache.amazonaws.com",
            port=6379,
            decode_responses=True,
            ssl=False,
        )
        redis.set("test", "hello from redis")
        value = redis.get("test")
        return {"Message": value}
    except Exception as e:
        return {"Message": e}


@app.get("/ping", name="Healthcheck", tags=["Healthcheck"])
async def healthcheck():
    return {"Success": "Pong!"}


app.include_router(api_router, prefix="/api/v1")

handler = Mangum(app)
