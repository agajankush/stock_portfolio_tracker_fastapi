from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import portfolios, users
from logging_config import setup_logging
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager
import asyncio
import random
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

setup_logging()

# Websocket test
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Application starting up...")
#     task = asyncio.create_task(periodic_broadcast())
#     yield
#     print("Application shutting down...")
#     task.cancel()
#     await task

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Stock Portfolio API",
    description="An API to manage user stock portfolios in real-time.",
    version="0.1.0",
    # lifespan=lifespan,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Websocket test
# async def periodic_broadcast():
#     while True:
#         print("Broadcasting message...")
#         await asyncio.sleep(3)
#         stock = random.choice(["AAPL", "GOOGL", "MSFT", "AMZN"])
#         price = round(random.uniform(150, 2000), 2)
#         update = {"stock": stock, "price": price}
#         print(f"Broadcasting update: {update}")
#         await portfolios.manager.broadcast(update)

Instrumentator().instrument(app).expose(app)

app.include_router(users.router)
app.include_router(portfolios.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Stock Portfolio API!"}
