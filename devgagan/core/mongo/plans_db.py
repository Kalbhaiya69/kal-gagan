# ---------------------------------------------------
# File Name: plans_db.py
# Description: Premium user management
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Created: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

import datetime

# In-memory storage for premium users
premium_data = {}


async def add_premium(user_id, expire_date):
    premium_data[user_id] = {"_id": user_id, "expire_date": expire_date}


async def remove_premium(user_id):
    if user_id in premium_data:
        del premium_data[user_id]


async def check_premium(user_id):
    return premium_data.get(user_id)


async def premium_users():
    return list(premium_data.keys())


async def check_and_remove_expired_users():
    current_time = datetime.datetime.utcnow()
    expired_users = []
    
    for user_id, data in premium_data.items():
        expire_date = data.get("expire_date")
        if expire_date and expire_date < current_time:
            expired_users.append(user_id)
    
    for user_id in expired_users:
        await remove_premium(user_id)
        print(f"Removed user {user_id} due to expired plan.")
