from fastapi import APIRouter, HTTPException
from app.models import users
from app.database import database
from app.schemas.user import UserCreate

router = APIRouter()


@router.post("/users/create")
async def create_new_user(user: UserCreate):
    query = users.insert().values(**user.dict())
    user_id = await database.execute(query)
    return {"id": user_id, "message": "User created successfully"}


@router.get("/user/{user_id}")
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/")
async def read_all_users():
    query = users.select()
    users_list = await database.fetch_all(query)
    return {"users": users_list}


@router.put("/user/{user_id}")
async def update_user_data(user_id: int, user: UserCreate):
    query = users.update().where(users.c.id == user_id).values(**user.dict())
    await database.execute(query)
    updated_user_query = users.select().where(users.c.id == user_id)
    updated_user = await database.fetch_one(updated_user_query)
    return updated_user


@router.delete("/user/{user_id}")
async def remove_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
