# ---------------------------------------------------
# File Name: users_db.py
# MongoDB based user storage (FINAL CLEAN VERSION)
# ---------------------------------------------------

from motor.motor_asyncio import AsyncIOMotorClient
from devgagan.config import MONGO_DB

MongoCli = AsyncIOMotorClient

mongo = MongoCli(MONGO_DB)
db = mongo.users.users_db


async def get_users():
    users = []
    async for doc in db.find({}, {"_id": 0, "user": 1}):
        users.append(doc["user"])
    return users


async def get_user(user: int) -> bool:
    return await db.find_one({"user": user}) is not None


async def add_user(user: int):
    if not await get_user(user):
        await db.insert_one({"user": user})


async def del_user(user: int):
    await db.delete_one({"user": user})
