# ---------------------------------------------------
# File Name: users_db.py
# Description: In-memory user management
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Created: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

# In-memory storage for users
users_set = set()

async def get_users():
    return list(users_set)

async def get_user(user):
    return user in users_set

async def add_user(user):
    users_set.add(user)

async def del_user(user):
    users_set.discard(user)port AsyncIOMotorClient as MongoCli


mongo = MongoCli(MONGO_DB)
db = mongo.users
db = db.users_db


async def get_users():
  user_list = []
  async for user in db.users.find({"user": {"$gt": 0}}):
    user_list.append(user['user'])
  return user_list


async def get_user(user):
  users = await get_users()
  if user in users:
    return True
  else:
    return False

async def add_user(user):
  users = await get_users()
  if user in users:
    return
  else:
    await db.users.insert_one({"user": user})


async def del_user(user):
  users = await get_users()
  if not user in users:
    return
  else:
    await db.users.delete_one({"user": user})
    


