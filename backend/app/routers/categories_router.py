from fastapi import APIRouter, HTTPException, status
from typing import List
from psycopg2.extras import DictCursor

from .. import schemas
from ..database import get_db_connection, release_db_connection

router = APIRouter(
    prefix='/categories',
    tags=['Categories']
)

@router.get("/", response_model=List[schemas.Categories], summary="Getting all categories data")
def get_all_categories():
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        query = "SELECT id, name, description FROM categories;"
        cursor.execute(query)
        categories = cursor.fetchall()

        cursor.close()

        return [dict(category) for category in categories]
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error accured: {str(e)}")
    finally:
        if conn:
            release_db_connection(conn)

@router.post("/", response_model=schemas.Categories, status_code=status.HTTP_201_CREATED, summary="Create Categories")
def create_new_categories(category: schemas.CategoriesCreate):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        query_insert = """
        INSERT INTO categories(name, description)
        VALUES (%s, %s)
        RETURNING id, name, description;
        """

        cursor.execute(query_insert, (
            category.name,
            category.description,
        ))

        new_category = cursor.fetchone()
        conn.commit()

        cursor.close()

        return dict(new_category)
    except Exception as e:
        conn.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categories name already exists.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error accured: {str(e)}")
    finally:
        release_db_connection(conn)

@router.put("/{id}", response_model=schemas.Categories, status_code=status.HTTP_200_OK, summary="Edit or Update categories value")
def update_record_value_categories(id: int, category: schemas.CategoriesCreate):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        # cursor.execute("SELECT id FROM categories WHERE id = %s;", (id,))
        # category = cursor.fetchone()

        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id: {id} not found.")
        
        query_update = """
        UPDATE categories
        SET name=%s, description=%s
        WHERE id = %s
        RETURNING *;
        """

        cursor.execute(query_update,(
            category.name,
            category.description,
            id
        ))

        updated_category_row = cursor.fetchone()

        if not updated_category_row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {id} not found.")

        conn.commit()

        cursor.close()
        return dict(updated_category_row)

    except Exception as e:
        conn.rollback()
        if isinstance(e, HTTPException):
            raise e
        if "violates foreign key constraint" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categories with id: {id} not found.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")
    finally:
        release_db_connection(conn)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a category")
def delete_category(id: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        # Running query delete and use returning id to check is there any have beeing delete cok?
        query_delete = "DELETE FROM categories WHERE id = %s RETURNING id;"
        cursor.execute(query_delete, (id,))

        deleted_category = cursor.fetchone()

        if not deleted_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id: {id} not found.")

        conn.commit()

        cursor.close()

        return None

    except Exception as e:
        conn.rollback()

        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category with id: {id} cannot be deleted because it is still in use by products.")

        if isinstance(e, HTTPException) and e.status_code == 404:
            raise e

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occured {str(e)}")
    
    finally:
        if conn:
            release_db_connection(conn)