from fastapi import APIRouter, HTTPException, status
from typing import List
from .. import schemas 
from ..database import get_db_connection, release_db_connection

router = APIRouter(
    prefix='/customers',
    tags=["Customers"]
)

@router.get("/", response_model=List[schemas.Customer])
def get_all_customer():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "SELECT id, first_name, last_name, username, phone_number, email, religion, gender, profile_picture FROM customers ORDER BY id ASC;"
        cursor.execute(query)
        customer_tuples = cursor.fetchall()