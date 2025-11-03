from fastapi import APIRouter, HTTPException, status
from typing import List
from psycopg2.extras import DictCursor # Import DictCursor


from .. import schemas 
from ..database import get_db_connection, release_db_connection
from ..utils import utils

router = APIRouter(
    prefix='/customers',
    tags=["Customers"]
)



@router.get("/", response_model=List[schemas.Customer], summary="Getting all customer datas")
def get_all_customers():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "SELECT id, first_name, last_name, username, phone_number, email, gender, profile_picture, created_at FROM customers ORDER BY id ASC;"
        cursor.execute(query)
        customer_tuples = cursor.fetchall()

        # convert result (list of tuples) menjadi list of dict
        customers = []
        for cust_tuple in customer_tuples:
            customers.append({
                "id": cust_tuple[0],
                "first_name": cust_tuple[1],
                "last_name": cust_tuple[2],
                "username": cust_tuple[3],
                "phone_number": cust_tuple[4],
                "email": cust_tuple[5],
                "gender": cust_tuple[6],
                "profile_picture": cust_tuple[7],
                "created_at": cust_tuple[8]
            })

        cursor.close()
        return customers
    finally:
        release_db_connection(conn)


@router.post("/", response_model=schemas.Customer, status_code=status.HTTP_201_CREATED, summary="Create an Customer")
def create_new_customer(customer: schemas.CustomerCreate):
    hashed_password = utils.hash_password(customer.password.get_secret_value())

    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        # note pengunaan %s untuk placeholder itu untuk keamanan untuk menghindari SQL Injection
        query = """
            INSERT INTO customers (first_name, last_name, username, hash_password, phone_number, email, gender, religion, profile_picture)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """
        cursor.execute(query, (
            customer.first_name,
            customer.last_name,
            customer.username,
            hashed_password,
            customer.phone_number,
            customer.email,
            customer.gender,
            customer.religion,
            str(customer.profile_picture) if customer.profile_picture else None
        ))

        new_customer_id = cursor.fetchone()['id']
        conn.commit() # simpan perubahan ke database
        
        query_select = "SELECT id, first_name, last_name, username, phone_number, email, gender, religion, profile_picture, created_at FROM customers WHERE id = %s;"
        cursor.execute(query_select, (new_customer_id,))
        new_customer = cursor.fetchone()

        # DEBUGGING
        # print("Tipe data new_customer:", type(new_customer)) 
        # print("Isi variabel new_customer:", new_customer)

        cursor.close()
        return dict(new_customer)
        
    except Exception as e:
        conn.rollback()
        # cek errror untuk duplikasi email / username
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or Username already exists.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        release_db_connection(conn)


# ==== Addresses ====
@router.get("/{customer_id}/addresses", response_model=List[schemas.Addresses], summary="Getting an address for a specific customer")
def get_all_customer_addresses(customer_id: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        # First, check if the customer exists to provide a clear 404 error
        cursor.execute("SELECT id FROM customers WHERE id = %s;", (customer_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer with id: {customer_id} not found.")

        # Fetch all addresses for the given customer_id
        query = "SELECT * FROM addresses WHERE customer_id = %s ORDER BY is_default DESC, id ASC;"
        cursor.execute(query, (customer_id,))
        addresses = cursor.fetchall()

        cursor.close()
        return [dict(address) for address in addresses]
    except Exception as e:
        # Re-raise HTTPException to avoid masking it as a 500 error
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")
    finally:
        release_db_connection(conn)



@router.post("/{customer_id}/addresses", response_model=schemas.Addresses, status_code=status.HTTP_201_CREATED, summary="Create an address for a specific customer")
def create_customer_address(customer_id: int, address: schemas.AddressesCreate):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        cursor.execute("SELECT id FROM customers WHERE id = %s;", (customer_id,))
        customer = cursor.fetchone()

        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with id: {customer_id} not found.")
        
        if address.is_default:
            query_update = """
                UPDATE addresses 
                SET is_default = FALSE 
                WHERE customer_id = %s AND is_default = TRUE;
            """
            cursor.execute(query_update, (customer_id,))

        query_insert = """
            INSERT INTO addresses(customer_id, address_line1, region, state_province, city, district, sub_district, address, zip_code, is_default)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """
        cursor.execute(query_insert, (
            customer_id,
            address.address_line1,
            address.region,
            address.state_province,
            address.city,
            address.district,
            address.sub_district,
            address.address,
            address.zip_code,
            address.is_default
        ))

        new_address_id = cursor.fetchone()['id']
        conn.commit()

        query_select = "SELECT * FROM addresses WHERE id = %s;"
        cursor.execute(query_select, (new_address_id,))
        new_address = cursor.fetchone()

        cursor.close()
        return dict(new_address)

    except Exception as e:
        conn.rollback()
        if isinstance(e, HTTPException):
            raise e
        if "violates foreign key constraint" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with id: {customer_id} not found.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")
    finally:
        release_db_connection(conn)