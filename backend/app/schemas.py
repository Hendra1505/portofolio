# schemas ini tujuannya untuk menghindari data yang salah dari front-end masuk ke backend, dan sebaliknya.
# Jadi, schemas memastikan integritas data yang berpindah antara front-end dan backend.

# Kita akan mendefinisikan "bentuk" data yang kita harapkan untuk masuk atau keluar dari API, tujuan nya untuk validasi bukan interaksi ke database
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Skema basic untuk produk, ini berjalan kalo kita mau membuat produk baru di sistem
class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    sku: str
    quantity_stock: int
    weight: Optional[float] = None
    length: Optional[float] = None
    width: Optional[float] = None
    brand_id: Optional[int] = None
    category_id: Optional[int] = None

# Skema lengkap termasuk 'id' yang bakal dikirim ke client
class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True # Membantu Pydantic bekerja dengan berbagai model data