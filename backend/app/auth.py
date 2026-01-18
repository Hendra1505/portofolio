import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from dotenv import load_dotenv

# Database and schema imports
from .database import get_db_connection, release_db_connection
from psycopg2.extras import DictCursor
from . import schemas


load_dotenv()

# --- Konfigurasi ---
SECRET_KEY = os.getenv("SECRET_KEY", "Key Does not exist")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# --- Fungsi-fungsi ---
def create_access_token(data: dict):
    """
    Membuat JWT access token baru.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    """
    Memverifikasi token, jika valid akan mengembalikan username.
    """
    try:
        TokenData = schemas.TokenData
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username)
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency yang akan menjadi "petugas keamanan".
    Ini akan dipanggil di setiap endpoint yang perlu diamankan.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token, credentials_exception)
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        query = "SELECT * FROM customers WHERE username = %s;"
        cursor.execute(query, (token_data.username,))
        user = cursor.fetchone()
        
        cursor.close()

        if user is None:
            raise credentials_exception
        
        return user
    finally:
        if conn:
            release_db_connection(conn)
