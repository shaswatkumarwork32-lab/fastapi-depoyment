import asyncio
import random
import time
from fastapi import FastAPI, Query, HTTPException

app = FastAPI(title="FastAPI Swarm Demo")

@app.get("/")
async def root():
    return {"message": "FastAPI running on Docker Swarm"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/latency")
async def latency(
    delay: float = Query(0, description="Delay in seconds"),
    fail: bool = Query(False, description="Force failure"),
    random_fail: int = Query(0, description="Failure percentage 0-100")
):
    start = time.time()

    if delay > 0:
        await asyncio.sleep(delay)

    if fail:
        raise HTTPException(status_code=500, detail="Forced failure")

    if random_fail > 0 and random.randint(1, 100) <= random_fail:
        raise HTTPException(status_code=500, detail="Random failure")

    return {
        "status": "success",
        "delay": delay,
        "time_taken": round(time.time() - start, 2)
    }


from fastapi.responses import HTMLResponse

@app.get("/version", response_class=HTMLResponse)
async def get_current_version():
    version = 1
    return f"<h1>{version}</h1>"