import time
import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas 
import database.models as models
import security
from database.database import get_db
from redis_client import redis_client
from celery_worker import generate_portfolio_report


router = APIRouter(
    prefix="/portfolios",
    tags=["portfolios"]
)

def get_current_user(token: str = Depends(security.oauth2_scheme), db: Session = Depends(get_db)):
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

@router.get("/stock/{ticker_symbol}/price")
def stock_price(symbol: str):
    cached_price = redis_client.get(symbol)
    
    if cached_price:
        return {"symbol": symbol, "price": cached_price, "source": "cache"}
    
    time.sleep(2)
    mock_price = random.uniform(random.uniform(100, 500), 2)
    
    redis_client.setex(symbol, 60, str(mock_price))
    return {"symbol": symbol, "price": mock_price, "source": "api"}

@router.post("/{portfolio_id}/report", status_code=status.HTTP_202_ACCEPTED)
def create_portfolio_report(portfolio_id: int):
    generate_portfolio_report.delay(portfolio_id, "user@example.com")
    return {"message": "Report generation started"}
