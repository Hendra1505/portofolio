from fastapi import APIRouter, HTTPException, status
from typing import List
from psycopg2.extras import DictCursor

from .. import schemas
from ..database import get_db_connection, release_db_connection


@router.get("/{customer_id}")