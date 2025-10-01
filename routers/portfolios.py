import random
import time

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

import database.models as models
import security
from celery_worker import generate_portfolio_report
from database.database import get_db
from redis_client import redis_client
import schemas
import crud
from connection_manager import ConnectionManager

router = APIRouter(prefix="/portfolios", tags=["portfolios"])
manager = ConnectionManager()

"""
INFO:
This router is used to manage the portfolios of the users.
It includes the endpoints to create a portfolio, get a portfolio, update a portfolio, and delete a portfolio.
"""

# Websocket endpoint
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Client sent: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        print("Client disconnected")

# Create a portfolio
@router.post("/", response_model=schemas.Portfolio)
def create_portfolio(
    portfolio: schemas.PortfolioCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    print(f"Creating portfolio for user: {current_user.email}")
    return {"name": portfolio.name, "description": portfolio.description, "id": 1, "user_id": current_user.id}

# Get the current user
def get_current_user(
    token: str = Depends(security.oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = security.verify_token(token, credentials_exception)
    # The token contains the user email in the 'sub' field
    user_email = token_data.get("sub")
    if user_email is None:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == user_email).first()
    if user is None:
        raise credentials_exception
    return user


# Get the stock price
@router.get("/stock/{ticker_symbol}/price")
def stock_price(symbol: str):
    cached_price = redis_client.get(symbol)

    if cached_price:
        return {"symbol": symbol, "price": cached_price, "source": "cache"}

    time.sleep(2)
    mock_price = random.uniform(random.uniform(100, 500), 2)

    redis_client.setex(symbol, 60, str(mock_price))
    return {"symbol": symbol, "price": mock_price, "source": "api"}


# Create a portfolio report
@router.post("/{portfolio_id}/report", status_code=status.HTTP_202_ACCEPTED)
def create_portfolio_report(portfolio_id: int):
    generate_portfolio_report.delay(portfolio_id, "user@example.com")
    return {"message": "Report generation started"}
