# main.py

from fastapi import FastAPI
# Corrected import without the dot
from routers import users, portfolios

app = FastAPI(
    title="Stock Portfolio API",
    description="An API to manage user stock portfolios in real-time.",
    version="0.1.0",
)

app.include_router(users.router)
app.include_router(portfolios.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Stock Portfolio API!"}