from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from psycopg2.extras import DictCursor

from .. import schemas, auth
from ..database import get_db_connection, release_db_connection

router = APIRouter(
    prefix='/cart',
    tags=['Cart Items']
)

@router.get("/me", response_model=List[schemas.CartItem], summary="Getting the authenticated customer's cart")
def get_my_cart(current_user: dict = Depends(auth.get_current_user)):
    """
    Mengambil semua item di keranjang milik pengguna yang sedang login.
    ID pengguna diambil dari token autentikasi.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        customer_id = current_user['id']

        query = "SELECT * FROM cart_items WHERE customer_id = %s ORDER BY created_at DESC;"
        cursor.execute(query, (customer_id,))
        cart_items = cursor.fetchall()

        cursor.close()
        return [dict(item) for item in cart_items]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")
    finally:
        if conn:
            release_db_connection(conn)

@router.post("/me/items", response_model=schemas.CartItem, status_code=status.HTTP_201_CREATED, summary="Add an item to the cart")
def add_item_to_cart(cart_item: schemas.CartItemCreate, current_user: dict = Depends(auth.get_current_user)):
    """
    Menambahkan item baru ke keranjang milik pengguna yang sedang login.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)
        customer_id = current_user['id']

        # Opsional: Cek apakah produk sudah ada di keranjang, jika ya, update quantity saja.
        # Untuk sekarang, kita langsung insert saja.
        query = """
            INSERT INTO cart_items (product_id, customer_id, quantity) 
            VALUES (%s, %s, %s)
            RETURNING *;
        """
        cursor.execute(query, (
            cart_item.product_id,
            customer_id,
            cart_item.quantity
        ))
        new_cart_item = cursor.fetchone()
        conn.commit()
        cursor.close()

        if not new_cart_item:
            raise HTTPException(status_code=500, detail="Failed to create cart item.")

        return dict(new_cart_item)
    except Exception as e:
        conn.rollback()
        # Handle specific database errors, e.g., product_id not found
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")
    finally:
        if conn:
            release_db_connection(conn)

@router.delete("/me/items/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove an item from the cart")
def remove_item_from_cart(cart_item_id: int, current_user: dict = Depends(auth.get_current_user)):
    """
    Menghapus sebuah item dari keranjang milik pengguna yang sedang login.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)
        customer_id = current_user['id']

        # Hapus item hanya jika item tersebut milik user yang benar
        query_delete = "DELETE FROM cart_items WHERE id = %s AND customer_id = %s RETURNING id;"
        cursor.execute(query_delete, (cart_item_id, customer_id))

        deleted_item = cursor.fetchone()

        if not deleted_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cart item with id: {cart_item_id} not found in your cart.")
        
        conn.commit()
        cursor.close()
        return None
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")
    finally:
        if conn:
            release_db_connection(conn)