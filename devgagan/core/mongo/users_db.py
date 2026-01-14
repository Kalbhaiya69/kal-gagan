# ---------------------------------------------------
# File Name: users_db.py
# Description: MongoDB user management
# ---------------------------------------------------

from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from devgagan.config import MONGO_DB

mongo = MongoCli(MONGO_DB)
db = mongo.users_db


async def get_users():
    user_list = []
    async for user in db.users.find({"user": {"$gt": 0}}):
        user_list.append(user["user"])
    return user_list


async def get_user(user):
    users = await get_users()
    return user in users


async def add_user(user):
    users = await get_users()
    if user in users:
        return
    await db.users.insert_one({"user": user})


async def del_user(user):
    users = await get_users()
    if user not in users:
        return
    await db.users.delete_one({"user": user})
