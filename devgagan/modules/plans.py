# ---------------------------------------------------
# File Name: plans.py
# Description: Premium plan management
# Author: Gagan
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

from datetime import timedelta
import pytz
import datetime
from devgagan import app
from config import OWNER_ID
from devgagan.core.func import get_seconds
from devgagan.core.mongo import plans_db  
from pyrogram import filters 

@app.on_message(filters.command("rem") & filters.user(OWNER_ID))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])  
        user = await client.get_users(user_id)
        data = await plans_db.check_premium(user_id)  
        
        if data and data.get("_id"):
            await plans_db.remove_premium(user_id)
            await message.reply_text("User removed successfully!")
            await client.send_message(
                chat_id=user_id,
                text=f"<b>Hey {user.mention},\n\nYour premium access has been removed.\nThank you for using our service 😊.</b>"
            )
        else:
            await message.reply_text("Unable to remove user!\nAre you sure it was a premium user ID?")
    else:
        await message.reply_text("Usage: /rem user_id") 

@app.on_message(filters.command("myplan"))
async def myplan(client, message):
    user_id = message.from_user.id
    user = message.from_user.mention
    data = await plans_db.check_premium(user_id)  
    if data and data.get("expire_date"):
        expiry = data.get("expire_date")
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\nExpiry Time: %I:%M:%S %p")            
        
        current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        time_left = expiry_ist - current_time
            
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
            
        time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
        await message.reply_text(f"⚜️ Premium User Data:\n\n👤 User: {user}\n⚡ User ID: <code>{user_id}</code>\n⏰ Time Left: {time_left_str}\n⌛ Expiry Date: {expiry_str_in_ist}")   
    else:
        await message.reply_text(f"Hey {user},\n\nYou do not have any active premium plans")

@app.on_message(filters.command("check") & filters.user(OWNER_ID))
async def get_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        data = await plans_db.check_premium(user_id)  
        if data and data.get("expire_date"):
            expiry = data.get("expire_date") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\nExpiry Time: %I:%M:%S %p")            
            
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
            await message.reply_text(f"⚜️ Premium User Data:\n\n👤 User: {user.mention}\n⚡ User ID: <code>{user_id}</code>\n⏰ Time Left: {time_left_str}\n⌛ Expiry Date: {expiry_str_in_ist}")
        else:
            await message.reply_text("No premium data found in database!")
    else:
        await message.reply_text("Usage: /check user_id")

@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y\nJoining Time: %I:%M:%S %p") 
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        time = message.command[2]+" "+message.command[3]
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)  
            await plans_db.add_premium(user_id, expiry_time)  
            data = await plans_db.check_premium(user_id)
            expiry = data.get("expire_date")   
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\nExpiry Time: %I:%M:%S %p")         
            await message.reply_text(f"Premium added successfully ✅\n\n👤 User: {user.mention}\n⚡ User ID: <code>{user_id}</code>\n⏰ Premium Access: <code>{time}</code>\n\n⏳ Joining Date: {current_time}\n\n⌛ Expiry Date: {expiry_str_in_ist}\n\n__**Powered by @BADDY_15**__", disable_web_page_preview=True)
            await client.send_message(
                chat_id=user_id,
                text=f"👋 Hey {user.mention},\nThank you for purchasing premium.\nEnjoy!! ✨🎉\n\n⏰ Premium Access: <code>{time}</code>\n⏳ Joining Date: {current_time}\n\n⌛ Expiry Date: {expiry_str_in_ist}", disable_web_page_preview=True              
            )
        else:
            await message.reply_text("Invalid time format. Use: '1 day', '1 hour', '1 min', '1 month', or '1 year'")
    else:
        await message.reply_text("Usage: /add user_id time (e.g., '1 day', '1 hour', '1 min', '1 month', '1 year')")

@app.on_message(filters.command("transfer"))
async def transfer_premium(client, message):
    if len(message.command) == 2:
        new_user_id = int(message.command[1])
        sender_user_id = message.from_user.id
        sender_user = await client.get_users(sender_user_id)
        new_user = await client.get_users(new_user_id)
        
        data = await plans_db.check_premium(sender_user_id)
        
        if data and data.get("_id"):
            expiry = data.get("expire_date")  
            
            await plans_db.remove_premium(sender_user_id)
            await plans_db.add_premium(new_user_id, expiry)
            
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime(
                "%d-%m-%Y\n⏱️ **Expiry Time:** %I:%M:%S %p"
            )
            time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            current_time = time_zone.strftime("%d-%m-%Y\n⏱️ **Transfer Time:** %I:%M:%S %p")
            
            await message.reply_text(
                f"✅ **Premium Plan Transferred Successfully!**\n\n"
                f"👤 **From:** {sender_user.mention}\n"
                f"👤 **To:** {new_user.mention}\n"
                f"⏳ **Expiry Date:** {expiry_str_in_ist}\n\n"
                f"__Powered by @BADDY_15__ 🚀"
            )
            
            await client.send_message(
                chat_id=new_user_id,
                text=(
                    f"👋 **Hey {new_user.mention},**\n\n"
                    f"🎉 **Your Premium Plan has been Transferred!**\n"
                    f"🛡️ **Transferred From:** {sender_user.mention}\n\n"
                    f"⏳ **Expiry Date:** {expiry_str_in_ist}\n"
                    f"📅 **Transferred On:** {current_time}\n\n"
                    f"__Enjoy the Service!__ ✨"
                )
            )
        else:
            await message.reply_text("⚠️ **You are not a Premium user!**\n\nOnly Premium users can transfer their plans.")
    else:
        await message.reply_text("⚠️ **Usage:** /transfer user_id\n\nReplace `user_id` with the new user's ID.")

async def premium_remover():
    all_users = await plans_db.premium_users()
    removed_users = []
    not_removed_users = []

    for user_id in all_users:
        try:
            user = await app.get_users(user_id)
            chk_time = await plans_db.check_premium(user_id)

            if chk_time and chk_time.get("expire_date"):
                expiry_date = chk_time["expire_date"]

                if expiry_date <= datetime.datetime.now():
                    name = user.first_name
                    await plans_db.remove_premium(user_id)
                    await app.send_message(user_id, text=f"Hello {name}, your premium subscription has expired.")
                    print(f"{name}, your premium subscription has expired.")
                    removed_users.append(f"{name} ({user_id})")
                else:
                    name = user.first_name
                    current_time = datetime.datetime.now()
                    time_left = expiry_date - current_time

                    days = time_left.days
                    hours, remainder = divmod(time_left.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    if days > 0:
                        remaining_time = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
                    elif hours > 0:
                        remaining_time = f"{hours} hours, {minutes} minutes, {seconds} seconds"
                    elif minutes > 0:
                        remaining_time = f"{minutes} minutes, {seconds} seconds"
                    else:
                        remaining_time = f"{seconds} seconds"

                    print(f"{name}: Remaining Time: {remaining_time}")
                    not_removed_users.append(f"{name} ({user_id})")
        except:
            await plans_db.remove_premium(user_id)
            print(f"Unknown user captured: {user_id} removed")
            removed_users.append(f"Unknown ({user_id})")

    return removed_users, not_removed_users

@app.on_message(filters.command("freez") & filters.user(OWNER_ID))
async def refresh_users(_, message):
    removed_users, not_removed_users = await premium_remover()
    removed_text = "\n".join(removed_users) if removed_users else "No users removed."
    not_removed_text = "\n".join(not_removed_users) if not_removed_users else "No users remaining with premium."
    summary = (
        f"**Here is Summary...**\n\n"
        f"> **Removed Users:**\n{removed_text}\n\n"
        f"> **Not Removed Users:**\n{not_removed_text}"
    )
    await message.reply(summary)iption has expired.")
                    removed_users.append(f"{name} ({user_id})")
                else:
                    name = user.first_name
                    current_time = datetime.datetime.now()
                    time_left = expiry_date - current_time

                    days = time_left.days
                    hours, remainder = divmod(time_left.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    if days > 0:
                        remaining_time = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
                    elif hours > 0:
                        remaining_time = f"{hours} hours, {minutes} minutes, {seconds} seconds"
                    elif minutes > 0:
                        remaining_time = f"{minutes} minutes, {seconds} seconds"
                    else:
                        remaining_time = f"{seconds} seconds"

                    print(f"{name} : Remaining Time : {remaining_time}")
                    not_removed_users.append(f"{name} ({user_id})")
        except:
            await plans_db.remove_premium(user_id)
            print(f"Unknown users captured : {user_id} removed")
            removed_users.append(f"Unknown ({user_id})")

    return removed_users, not_removed_users


@app.on_message(filters.command("freez") & filters.user(OWNER_ID))
async def refresh_users(_, message):
    removed_users, not_removed_users = await premium_remover()
    # Create a summary message
    removed_text = "\n".join(removed_users) if removed_users else "No users removed."
    not_removed_text = "\n".join(not_removed_users) if not_removed_users else "No users remaining with premium."
    summary = (
        f"**Here is Summary...**\n\n"
        f"> **Removed Users:**\n{removed_text}\n\n"
        f"> **Not Removed Users:**\n{not_removed_text}"
    )
    await message.reply(summary)
    
