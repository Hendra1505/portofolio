# schemas ini tujuannya untuk menghindari data yang salah dari front-end masuk ke backend, dan sebaliknya.
# Jadi, schemas memastikan integritas data yang berpindah antara front-end dan backend.

# Kita akan mendefinisikan "bentuk" data yang kita harapkan untuk masuk atau keluar dari API, tujuan nya untuk validasi bukan interaksi ke database
from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr, Field
from typing import List, Optional
from datetime import datetime


# === Start Product ===
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
# === End Product ===


# === Start Customer ===
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    phone_number: str
    email: EmailStr
    gender: Optional[str] = None
    religion: Optional[str] = None
    profile_picture: Optional[HttpUrl] = None

class CustomerCreate(CustomerBase):
    password: SecretStr = Field(
        ...,
        min_length=8, # minimal 8 karakter
        max_length=72 # maksimal 72 karakter
    )
    # Tipe Data: SecretStr. Ini adalah tipe khusus dari Pydantic yang akan menyembunyikan 
    # nilai password di log atau pesan error, mencegah kebocoran yang tidak disengaja.

class Customer(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
# === End Customer ===


# === Start Addresses ===
class AddressesBase(BaseModel):
    address_line1: str
    region: str
    state_province: str
    city: str
    district: str
    sub_district: str
    address: str
    zip_code: int
    is_default: Optional[bool] = False

class Addresses(AddressesBase):
    id: int
    customer_id: int

    class Config:
        from_attributes = True
# === End Addresses ===


# === Start brands ===
class BrandsBase(BaseModel):
    name: str

class Brands(BrandsBase):
    id: int

    class Config:
        from_attributes = True
# === End brands ===


# === Start categories ===
class CategoriesBase(BaseModel):
    name: str

class Categories(CategoriesBase):
    id: int

    class Config:
        from_attributes = True

# === End categories ===


# === Start cart items ===
class CartItemBase(BaseModel):
    quantity: int

class CartItem(CartItemBase):
    id: int
    product_id: int
    customer_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
# === End cart items ===


# === Start orders ===
class OrdersBase(BaseModel):
    status: str

class Orders(OrdersBase):
    id: int
    customer_id: int

    class Config:
        from_attributes = True

# === End orders ===


# === Start order items ===
class OrderItemsBase(BaseModel):
    quantity: int
    price_at_purchase: float


class OrderItem(OrderItemsBase):
    id: int
    product_id: int
    order_id: int

    class Config:
        from_attributes = True
# === End order items ===


# === Start payments ===
class PaymentsBase(BaseModel):
    amount: float
    status: str

class Payments(PaymentsBase):
    id: int
    status: datetime
    order_id: int

    class Config:
        from_attributes = True