# ---------------------------------------------------
# File Name: users_db.py
# MongoDB based user storage (FINAL CLEAN VERSION)
# ---------------------------------------------------

from motor.motor_asyncio import AsyncIOMotorClient
from devgagan.config import MONGO_DB

# MongoDB Client Setup
client = AsyncIOMotorClient(MONGO_DB)
db = client["devgagan"]["users"]


async def get_users():
    """Get all user IDs from database"""
    users = []
    async for doc in db.find({}, {"_id": 0, "user": 1}):
        if "user" in doc:
            users.append(doc["user"])
    return users


async def get_user(user: int) -> bool:
    """Check if user exists in database"""
    found = await db.find_one({"user": user})
    return found is not None


async def add_user(user: int):
    """Add new user to database"""
    exists = await get_user(user)
    if not exists:
        await db.insert_one({"user": user})


async def del_user(user: int):
    """Delete user from database"""
    await db.delete_one({"user": user})
