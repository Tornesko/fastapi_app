from app.models import users, products, product_buyers
from app.database import database
from sqlalchemy import insert


async def fill_db():
    user_data = [
        {"username": "john_doe", "email": "john@example.com", "password": "securepassword",
         "card_number": "1234567812345678", "pin_code": "1234"},
        {"username": "alice_smith", "email": "alice@example.com", "password": "securepassword",
         "card_number": "8765432187654321", "pin_code": "5678"},
        {"username": "bob_jones", "email": "bob@example.com", "password": "securepassword",
         "card_number": "1122334455667788", "pin_code": "9876"},
        {"username": "linda_white", "email": "linda@example.com", "password": "securepassword",
         "card_number": "2233445566778899", "pin_code": "6543"},
        {"username": "charlie_brown", "email": "charlie@example.com", "password": "securepassword",
         "card_number": "3344556677889900", "pin_code": "4321"},
        {"username": "emily_davis", "email": "emily@example.com", "password": "securepassword",
         "card_number": "4455667788990011", "pin_code": "3210"},
        {"username": "david_moore", "email": "david@example.com", "password": "securepassword",
         "card_number": "5566778899001122", "pin_code": "2109"},
    ]
    for user in user_data:
        await database.execute(insert(users).values(user))

    product_data = [
        {"title": "Laptop", "price": 999.99, "description": "A powerful laptop with 16GB RAM and 512GB SSD",
         "quantity": 10, "owner_id": 1},
        {"title": "Smartphone", "price": 499.99, "description": "A great smartphone with a 6.5-inch display",
         "quantity": 15, "owner_id": 2},
        {"title": "Smartwatch", "price": 199.99, "description": "A stylish smartwatch with fitness tracking",
         "quantity": 25, "owner_id": 3},
        {"title": "Bluetooth Headphones", "price": 59.99, "description": "Noise-cancelling Bluetooth headphones",
         "quantity": 50, "owner_id": 4},
        {"title": "4K TV", "price": 799.99, "description": "A 55-inch 4K UHD Smart TV with HDR", "quantity": 5,
         "owner_id": 5},
        {"title": "Gaming Chair", "price": 149.99, "description": "Ergonomic gaming chair for comfort", "quantity": 20,
         "owner_id": 6},
        {"title": "Air Purifier", "price": 99.99, "description": "A HEPA air purifier for clean air", "quantity": 30,
         "owner_id": 7},
        {"title": "Electric Toothbrush", "price": 29.99,
         "description": "Sonic electric toothbrush for better oral care", "quantity": 40, "owner_id": 1},
        {"title": "Portable Speaker", "price": 79.99, "description": "Bluetooth portable speaker with deep bass",
         "quantity": 35, "owner_id": 2},
        {"title": "Digital Camera", "price": 349.99, "description": "High-quality digital camera with 20MP resolution",
         "quantity": 10, "owner_id": 3},
        {"title": "Laptop Backpack", "price": 39.99, "description": "A stylish and durable backpack for your laptop",
         "quantity": 15, "owner_id": 4},
        {"title": "Electric Kettle", "price": 49.99, "description": "1.7L electric kettle with quick boiling feature",
         "quantity": 25, "owner_id": 5},
    ]
    for product in product_data:
        product["slug"] = product["title"].lower().replace(" ", "-")
        await database.execute(insert(products).values(product))

    product_buyers_data = [
        {"product_id": 1, "user_id": 2},
        {"product_id": 2, "user_id": 1},
        {"product_id": 3, "user_id": 4},
        {"product_id": 4, "user_id": 3},
        {"product_id": 5, "user_id": 5},
        {"product_id": 6, "user_id": 2},
        {"product_id": 7, "user_id": 1},
        {"product_id": 8, "user_id": 6},
        {"product_id": 9, "user_id": 7},
        {"product_id": 10, "user_id": 4},
        {"product_id": 11, "user_id": 5},
        {"product_id": 12, "user_id": 1},
    ]
    for buyer in product_buyers_data:
        await database.execute(insert(product_buyers).values(buyer))

    print("Database has been populated with test data.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(fill_db())
