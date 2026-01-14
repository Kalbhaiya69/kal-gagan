# ---------------------------------------------------
# File Name: db.py
# Description: In-memory data storage for user settings
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Created: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

# In-memory storage (data will reset on bot restart)
user_data = {}

async def get_data(user_id):
    return user_data.get(user_id, {})

async def set_thumbnail(user_id, thumb):
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["thumb"] = thumb

async def set_caption(user_id, caption):
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["caption"] = caption

async def replace_caption(user_id, replace_txt, to_replace):
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["replace_txt"] = replace_txt
    user_data[user_id]["to_replace"] = to_replace

async def set_session(user_id, session):
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["session"] = session

async def clean_words(user_id, new_clean_words):
    if user_id not in user_data:
        user_data[user_id] = {}
    existing_words = user_data[user_id].get("clean_words", [])
    user_data[user_id]["clean_words"] = list(set(existing_words + new_clean_words))

async def remove_clean_words(user_id, words_to_remove):
    if user_id not in user_data:
        user_data[user_id] = {}
    existing_words = user_data[user_id].get("clean_words", [])
    user_data[user_id]["clean_words"] = [word for word in existing_words if word not in words_to_remove]

async def set_channel(user_id, chat_id):
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["chat_id"] = chat_id

async def all_words_remove(user_id):
    if user_id in user_data:
        user_data[user_id]["clean_words"] = None

async def remove_thumbnail(user_id):
    if user_id in user_data:
        user_data[user_id]["thumb"] = None

async def remove_caption(user_id):
    if user_id in user_data:
        user_data[user_id]["caption"] = None

async def remove_replace(user_id):
    if user_id in user_data:
        user_data[user_id]["replace_txt"] = None
        user_data[user_id]["to_replace"] = None

async def remove_session(user_id):
    if user_id in user_data:
        user_data[user_id]["session"] = None

async def remove_channel(user_id):
    if user_id in user_data:
        user_data[user_id]["chat_id"] = None

async def delete_session(user_id):
    if user_id in user_data and "session" in user_data[user_id]:
        del user_data[user_id]["session"]t": {"clean_words": updated_words}})
    else:
        await db.insert_one({"_id": user_id, "clean_words": []})
async def set_channel(user_id, chat_id):
    data = await get_data(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"chat_id": chat_id}})
    else:
        await db.insert_one({"_id": user_id, "chat_id": chat_id})
async def all_words_remove(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"clean_words": None}})
async def remove_thumbnail(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"thumb": None}})
async def remove_caption(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"caption": None}})
async def remove_replace(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"replace_txt": None, "to_replace": None}})
 
async def remove_session(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"session": None}})
async def remove_channel(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"chat_id": None}})
async def delete_session(user_id):
    """Delete the session associated with the given user_id from the database."""
    await db.update_one({"_id": user_id}, {"$unset": {"session": ""}})
 