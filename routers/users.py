import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database.models as models
import schemas
import security
from database.database import engine, get_db
import crud

logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    new_user = crud.create_user(db, user)
    logger.info("New user created", extra={"email": user.email, "user_id": new_user.id})
    return new_user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    logger.info("User logged in", extra={"email": form_data.username})
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Ensure JWT_EXPIRATION_TIME is an int (in case it's a string from env)
    try:
        expiration_minutes = int(security.JWT_EXPIRATION_TIME)
    except (TypeError, ValueError):
        expiration_minutes = 15  # fallback default
    access_token_expires = timedelta(minutes=expiration_minutes)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
