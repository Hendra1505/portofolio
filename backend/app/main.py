from fastapi import FastAPI
from .routers import product_router, customer_router, brand_router

app = FastAPI(
    title="Rest API untuk E-commerce UMKM",
    description="API untuk mengelola produk, pesanan, dan customer",
    version="0.1.0"
)

# Register router produk
app.include_router(product_router.router)
# Register router customer dan address buat customer ya guys ya
app.include_router(customer_router.router)
# Register router brands
app.include_router(brand_router.router)
# Register router categories

@app.get("/")
def read_root():
    return {"message": "Welcome to API for UMKM E-Commerce"}

# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}