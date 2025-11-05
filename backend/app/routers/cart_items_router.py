from fastapi import APIRouter, HTTPException, status
from typing import List
from psycopg2.extras import DictCursor

from .. import schemas
from ..database import get_db_connection, release_db_connection

router = APIRouter(
    prefix='/carts',
    tags=['Cart Items']
)


@router.get("/{customer_id}", response_model=List[schemas.CartItem], summary="Getting cart datas")
def get_customer_cart(customer_id: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        cursor.execute("SELECT id FROM customers WHERE id = %s;", (customer_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer with id: {customer_id} not found.")

        query = "SELECT * FROM cart_items WHERE customer_id = %s ORDER BY created_at DESC;"
        cursor.execute(query, (customer_id,))
        cart_item_updated = cursor.fetchall()

        cursor.close()
        
        return [dict(item) for item in cart_item_updated]
    except Exception as e:
        conn.rollback()
        if isinstance(e, HTTPException):
                raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"An unexpected error occurred: {str(e)}")

    finally:
        if conn:
            release_db_connection(conn)