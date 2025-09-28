from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import schemas
import security
from datetime import timedelta

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# In-memory database placeholder
fast_users_db = {}

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate):
    # Check if user already exists
    if user.email in fast_users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    # Hash password
    hashed_password = security.get_password_hash(user.password)
    print(hashed_password)
    user_id = len(fast_users_db) + 1
    
    # Create user
    fast_users_db[user.email] = {
        "id": user_id,
        "email": user.email,
        "hashed_password": hashed_password
    }
    return {"id": user_id, "email": user.email}

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fast_users_db.get(form_data.username)
    if not user or not security.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=security.JWT_EXPIRATION_TIME)
    access_token = security.create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}