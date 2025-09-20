import os
import psycopg2
from pathlib import Path
from psycopg2 import pool
from dotenv import load_dotenv

# membuat variabel dari file .env
load_dotenv()

# membuat connection pool
db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=50,
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    dbname=os.getenv("DB_NAME")
)

def get_db_connection():
    """Mengambil koneksi dari pool."""
    return db_pool.getconn()

def release_db_connection(conn):
    """Mengembalikan koneksi ke pool"""
    db_pool.putconn(conn)


