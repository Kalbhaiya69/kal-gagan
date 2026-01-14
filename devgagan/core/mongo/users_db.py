from motor.motor_asyncio import AsyncIOMotorClient
from devgagan.config import MONGO_DB

client = AsyncIOMotorClient(MONGO_DB)
db = client["devgagan"]["users"]


async def get_users():
    users = []
    async for doc in db.find({}, {"_id": 0, "user": 1}):
        if "user" in doc:
            users.append(doc["user"])
    return users


async def get_user(user: int) -> bool:
    found = await db.find_one({"user": user})
    return found is not None


async def add_user(user: int):
    exists = await get_user(user)
    if not exists:
        await db.insert_one({"user": user})


async def del_user(user: int):
    await db.delete_one({"user": user})
