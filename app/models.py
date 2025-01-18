from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from app.database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("email", String, unique=True),
    Column("password", String),
    Column("card_number", String),
    Column("pin_code", String),
)

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("slug", String, unique=True),
    Column("price", Float),
    Column("description", String),
    Column("quantity", Integer),
    Column("owner_id", Integer, ForeignKey("users.id")),
)

product_buyers = Table(
    "product_buyers",
    metadata,
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)
