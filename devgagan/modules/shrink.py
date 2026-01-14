# ---------------------------------------------------
# File Name: shrink.py
# Description: Token verification and URL shortening
# Author: Gagan
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import string
import aiohttp
from devgagan import app
from devgagan.core.func import *
from datetime import datetime, timedelta
from config import WEBSITE_URL, AD_API, LOG_GROUP  

# In-memory storage for tokens
user_tokens = {}
Param = {}

async def generate_random_param(length=8):
    """Generate a random parameter."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def get_shortened_url(deep_link):
    api_url = f"https://{WEBSITE_URL}/api?api={AD_API}&url={deep_link}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()   
                if data.get("status") == "success":
                    return data.get("shortenedUrl")
    return None

async def is_user_verified(user_id):
    """Check if a user has an active session."""
    if user_id in user_tokens:
        expires_at = user_tokens[user_id]["expires_at"]
        if datetime.utcnow() < expires_at:
            return True
        else:
            del user_tokens[user_id]
    return False

@app.on_message(filters.command("start"))
async def token_handler(client, message):
    """Handle the /start command."""
    join = await subscribe(client, message)
    if join == 1:
        return
    
    user_id = message.chat.id
    
    if len(message.command) <= 1:
        join_button = InlineKeyboardButton("Join Channel", url="https://t.me/+0rEj-Cp7bBQ0YmU1")
        premium = InlineKeyboardButton("Get Premium", url="https://t.me/BADDY_15")   
        keyboard = InlineKeyboardMarkup([
            [join_button],   
            [premium]    
        ])
        
        await message.reply_photo(
            "https://graph.org/file/3eddaf2b77f5e2352640b-1cf1914d750ca43925.jpg",
            caption=(
                "Hi 👋 Welcome!\n\n"
                "✳️ I can save posts from channels/groups where forwarding is off. I can download videos/audio from YT, INSTA, and other platforms.\n"
                "✳️ Send the post link of a public channel. For private channels, do /login. Send /help to know more."
            ),
            reply_markup=keyboard
        )
        return  
 
    param = message.command[1]
    freecheck = await chk_user(message, user_id)
    
    if freecheck != 1:
        await message.reply("You are a premium user. Contact @BADDY_15")
        return
    
    if param:
        if user_id in Param and Param[user_id] == param:
            user_tokens[user_id] = {
                "param": param,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=3),
            }
            del Param[user_id]
            await message.reply("✅ You have been verified successfully! Enjoy your session for 3 hours.")
            return
        else:
            await message.reply("❌ Invalid or expired verification link. Please generate a new token.")
            return

@app.on_message(filters.command("token"))
async def smart_handler(client, message):
    user_id = message.chat.id
    
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user, no need for a token 😉")
        return
    
    if await is_user_verified(user_id):
        await message.reply("✅ Your free session is already active, enjoy!")
    else:
        param = await generate_random_param()
        Param[user_id] = param
        
        deep_link = f"https://t.me/{client.me.username}?start={param}"
        
        shortened_url = await get_shortened_url(deep_link)
        if not shortened_url:
            await message.reply("❌ Failed to generate the token link. Please try again.")
            return
        
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Verify the token now...", url=shortened_url)]]
        )
        await message.reply(
            "Click the button below to verify your free access token:\n\n"
            "> What will you get?\n"
            "1. No time bound for 3 hours\n"
            "2. Batch limit: FreeLimit + 20\n"
            "3. All functions unlocked", 
            reply_markup=button
        )      shortened_url = await get_shortened_url(deep_link)
        if not shortened_url:
            await message.reply("❌ Failed to generate the token link. Please try again.")
            return
 
         
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Verify the token now...", url=shortened_url)]]
        )
        await message.reply("Click the button below to verify your free access token: \n\n> What will you get ? \n1. No time bound upto 3 hours \n2. Batch command limit will be FreeLimit + 20 \n3. All functions unlocked", reply_markup=button)
 
