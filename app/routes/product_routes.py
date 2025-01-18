from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from app.models import products, users, product_buyers
from app.database import database
from app.schemas.product import ProductCreate, ProductUpdate, BuyProductRequest
from app.websocket_manager import websocket_manager

router = APIRouter()


@router.post("/products/create")
async def create_new_product(request: Request, product: ProductCreate):
    user_query = users.select().where(users.c.id == product.owner_id)
    user = await database.fetch_one(user_query)

    if not user:
        raise HTTPException(status_code=404, detail="Creator not found")

    query = products.insert().values(**product.dict())
    product_id = await database.execute(query)

    product_query = products.select().where(products.c.id == product_id)
    created_product = await database.fetch_one(product_query)

    overall_sum = created_product['price'] * created_product['quantity']

    counter = created_product['quantity']

    user_info = f"Amount: {counter}\n Overall sum: {overall_sum}"

    base_url = f"{request.url.scheme}://{request.url.hostname}"
    product_link = f"{base_url}/api/products/{product_id}"
    creator_link = f"{base_url}/api/users/{product.owner_id}"
    created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    notification = (
        f"Product: {product_link} Was added by {creator_link} at {created_at}"
    )

    await websocket_manager.send_message(notification)

    return {"id": product_id, "message": "Product created successfully", "user_info": user_info}


@router.get("/product/{product_id}")
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    product = await database.fetch_one(query)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/products/")
async def read_all_products(user_id: int = None):
    if user_id:
        query = products.select().where(products.c.owner_id == user_id)
    else:
        query = products.select()
    products_list = await database.fetch_all(query)
    return {"products": products_list}


@router.put("/product/{product_id}")
async def update_product_data(product_id: int, product: ProductUpdate):
    query = products.update().where(products.c.id == product_id).values(**product.dict())
    await database.execute(query)

    updated_product_query = products.select().where(products.c.id == product_id)
    updated_product = await database.fetch_one(updated_product_query)
    return updated_product


@router.delete("/product/{product_id}")
async def remove_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


@router.post("/product/{product_id}/buy")
async def buy_product(product_id: int, request: BuyProductRequest):
    user_id = request.user_id
    product_query = products.select().where(products.c.id == product_id)
    product = await database.fetch_one(product_query)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product['quantity'] <= 0:
        raise HTTPException(status_code=400, detail="Product out of stock")

    buyer_query = product_buyers.select().where(
        product_buyers.c.product_id == product_id, product_buyers.c.user_id == user_id
    )
    buyer = await database.fetch_one(buyer_query)

    if buyer:
        raise HTTPException(status_code=400, detail="User already bought this product")

    insert_query = product_buyers.insert().values(product_id=product_id, user_id=user_id)
    await database.execute(insert_query)

    update_query = products.update().where(products.c.id == product_id).values(quantity=product['quantity'] - 1)
    await database.execute(update_query)

    return {"message": f"Product {product_id} bought by user {user_id}"}
