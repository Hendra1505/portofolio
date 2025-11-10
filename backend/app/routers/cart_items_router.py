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


@router.post("/{customer_id}/cart/items", response_model=schemas.CartItem, summary="Create Cart Item")
def create_new_cart_item(customer_id: int, cart_item: schemas.CartItemCreate):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        query = """
            INSERT INTO cart_items (product_id, customer_id, quantity) 
            VALUES (%s,%s,%s)
            RETURNING *;
        """

        cursor.execute(query, (
            cart_item.product_id,
            customer_id,
            cart_item.quantity
        ))

        new_cart_item_row = cursor.fetchone()
        conn.commit()
        cursor.close()

        if not new_cart_item_row:
            raise HTTPException(status_code=500, detail="Failed to create cart item.")

        return dict(new_cart_item_row)

    except Exception as e:
        if "unique constraint" in str(e).lower():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or Username already exists.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        if conn:
            release_db_connection(conn)


@router.patch("/{customer_id}/cart/items", response_model=schemas.CartItem, summary="Edit Customer cart items")
def partially_update_record_customer_data_items(customer_id: int, cart_item: schemas.CustomerUpdate):
    conn = get_db_connection()

    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        update_data = cart_item.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There is No Field provided for update.")

        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])

        values = list(update_data.values())

        values.append(customer_id)

        query_update = f"""
            UPDATE cart_items
            SET {set_clause}
            WHERE id = %s
            RETURNING *;
        """

        cursor.execute(query_update, tuple(values))
        updated_cart_item = cursor_fetchone()

        if not updated_cart_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with id: {customer_id} not found")

        conn.commit()
        cursor.close()

        return dict(updated_cart_item)
    except Exception as e:
        conn.rollback()
        if isinstance(e, HTTPException):
                raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")
    finally:
        if conn:
            release_db_connection(conn)