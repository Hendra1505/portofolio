from fastapi import APIRouter, HTTPException, status
from .. import schemas # import schemas pydantic yang kita buat
from ..database import get_db_connection, release_db_connection
from typing import List

router = APIRouter(
    prefix='/products',
    tags=["Products"]
)

@router.get("/", response_model=List[schemas.Product])
def get_all_product():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "SELECT id, name, price, description, sku, quantity_stock, weight, length, width, created_at, brand_id, category_id FROM products ORDER BY id ASC;"
        cursor.execute(query)
        products_tuples = cursor.fetchall()

        # konversi hasil (list of tuples) menjadi list of dictionaries
        products = []
        for prod_tuple in products_tuples:
            products.append({
                "id": prod_tuple[0],
                "name": prod_tuple[1],
                "price": prod_tuple[2],
                "description": prod_tuple[3],
                "sku": prod_tuple[4],
                "quantity_stock": prod_tuple[5],
                "weight": prod_tuple[6],
                "length": prod_tuple[7],
                "width": prod_tuple[8],
                "created_at": prod_tuple[9],
                "brand_id": prod_tuple[10],
                "category_id": prod_tuple[11]  
            })

        cursor.close()
        return products
    finally:
        release_db_connection(conn)


@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductBase):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # penggunaan %s untuk placeholder demi keamanan (ngehindari SQL Injection)
        query = """
            INSERT INTO products (name, price, description, sku, quantity_stock, weight, length, width, brand_id, category_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id ASC;
            """
        cursor.execute(query, (
            product.name,
            product.price,
            product.description,
            product.sku,
            product.quantity_stock,
            product.weight,
            product.length,
            product.width,
            product.brand_id,
            product.category_id
        ))

        new_product_id = cursor.fetchone()[0]
        conn.commit() # simpan perubahan ke database
        cursor.close()

        # buat dictionary response sesuai skema product
        response_product = product.dict()
        response_product['id'] = new_product_id
        return response_product

    except Exception as e:
        conn.rollback() # Batalkan perubahan jika ada error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        release_db_connection(conn)