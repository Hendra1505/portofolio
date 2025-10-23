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