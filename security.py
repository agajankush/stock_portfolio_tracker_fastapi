# security.py

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import dotenv

dotenv.load_dotenv()

import os

# --- Configuration ---

# This key should be kept secret and loaded from an environment variable in a real application.
# You can generate a strong secret key using: openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
JWT_EXPIRATION_TIME = os.getenv("JWT_EXPIRATION_TIME")

# --- OAuth2 Setup ---

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

# --- Password Hashing Setup ---

# We use Argon2 as the hashing algorithm (no 72-byte limit like bcrypt)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# --- Helper Functions ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies that a plain password matches a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password using bcrypt."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a new JWT access token.
    The 'sub' (subject) of the token is typically the user's ID or email.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default expiration time if none is provided
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception: HTTPException):
    """
    Verifies a JWT token and returns the token data.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception