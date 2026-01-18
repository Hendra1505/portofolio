from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from psycopg2.extras import DictCursor

from .. import schemas
from ..database import get_db_connection, release_db_connection
from ..utils import utils
from .. import auth

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint untuk login user.
    Menerima form data dengan 'username' dan 'password'.
    Mengembalikan access token jika kredensial valid.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        # 1. Cari user di database berdasarkan username
        query = "SELECT id, username, hash_password FROM customers WHERE username = %s;"
        cursor.execute(query, (form_data.username,))
        customer = cursor.fetchone()

        # 2. Jika user tidak ditemukan atau password salah, kirim error
        if not customer or not utils.verify_password(form_data.password, customer['hash_password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 3. Jika berhasil, buat access token
        access_token = auth.create_access_token(
            data={"sub": customer['username'], "customer_id": customer['id']}
        )
        
        # 4. Kembalikan token
        return {"access_token": access_token, "token_type": "bearer"}

    finally:
        if conn:
            release_db_connection(conn)
