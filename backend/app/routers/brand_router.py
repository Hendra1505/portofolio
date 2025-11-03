from fastapi import APIRouter, HTTPException, status
from typing import List
from psycopg2.extras import DictCursor

from .. import schemas
from ..database import get_db_connection, release_db_connection

router = APIRouter(
    prefix='/brands',
    tags=['Brands']
)

@router.get("/", response_model=List[schemas.Brands], summary="Getting all brands data")
def get_all_brands():
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        query = "SELECT id, name FROM brands;"
        cursor.execute(query)
        brands = cursor.fetchall()

        cursor.close()
        return [dict(brand) for brand in brands]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occured: {str(e)}")
    finally:
        release_db_connection(conn)


@router.post("/", response_model=schemas.Brands, status_code=status.HTTP_201_CREATED, summary="Create an Brand")
def create_new_brand(brand: schemas.BrandCreate):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        query_insert = """
        INSERT INTO brands(name)
        VALUES (%s)
        RETURNING id, name;
        """

        cursor.execute(query_insert, (
            brand.name,
        ))

        new_brand = cursor.fetchone()
        conn.commit()

        # query_select = "SELECT * FROM brands;"
        # cursor.execute(query_select, (new_brand,))
        cursor.close()

        return dict(new_brand)

    except Exception as e:
        conn.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Brand name already exists.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}") 
    finally:
        release_db_connection(conn)
        

@router.put("/{id}", response_model=schemas.Brands, status_code=status.HTTP_200_OK, summary="Edit or Update brand value")
def update_record_value_brands(id:int, brand: schemas.BrandCreate):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factor=DictCursor)

        if not brand:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Brand with id: {id} not found.")

        query_update = """
        UPDATE brands
        SET name=%s
        WHERE id = %s
        RETURNING *;
        """

        cursor.execute(query_update, (
            brand.name,
            id
        ))

        updated_brand_row = cursor.fetchone()

        if not updated_brand_row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Brand with id: {id} not found.")
        
        conn.commit()

        cursor.close()
        return dict(updated_brand_row)
    except Exception as e:
        conn.rollback()
        if isinstance(e, HTTPException):
            raise e
        if "violates foreign key constraint" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Brand with id: {id} not found.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error accured: {str(e)}")
    finally:
        release_db_connection(conn)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Deleting a Brand")
def delete_brand(id: int):
    conn = get_db_connection()

    try:
        cursor = conn.cursor(cursory_factory=DictCursor)

        query_delete = "DELETE FROM brands WHERE id = %s RETURNING id;"
        cursor.execute(query_delete, (id,))

        deleted_brand = cursof.fetchone()

        if not deleted_brand:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Brand with id: {id} not found.")
        
        conn.commit()
        cursor.close()
        
        return None
    
    except Exception as e:
        conn.rollback()

        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Brand with id: {id} cannot deleted because is still in use by products.")
        
        if ininstance(e, HTTPException) and e.status_code == 404:
            raise e
        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occured {str(e)}")
    finally:
        if conn:
            release_db_connection(conn)