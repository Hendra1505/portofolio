from fastapi import FastAPI
from .routers import product_router

app = FastAPI(
    title="Rest API untuk E-commerce UMKM",
    description="API untuk mengelola produk, pesanan, dan customer",
    version="0.1.0"
)

# Daftarkan router produk ke aplikasi utama
app.include_router(product_router.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to API for UMKM E-Commerce"}

# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}