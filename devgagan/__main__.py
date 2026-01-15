# ---------------------------------------------------
# File Name: __main__.py
# Description: Pyrogram bot with web server for Render
# ---------------------------------------------------

import asyncio
import importlib
import gc
from threading import Thread
from pyrogram import idle
from devgagan import restrict_bot
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users

# Simple web server for Render
def run_web_server():
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Bot is running!')
        
        def log_message(self, format, *args):
            pass  # Suppress logs
    
    server = HTTPServer(('0.0.0.0', 10000), Handler)
    server.serve_forever()


async def schedule_expiry_check():
    while True:
        try:
            await check_and_remove_expired_users()
        except Exception as e:
            print(f"Error in expiry check: {e}")
        await asyncio.sleep(3600)  # Check every hour
        gc.collect()


async def devggn_boot():
    await restrict_bot()
    
    for all_module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + all_module)
    
    print("""
---------------------------------------------------
📂 Bot Deployed successfully ...
👨‍💻 Author: Gagan
🌐 GitHub: https://github.com/devgaganin/
📬 Telegram: https://t.me/team_spy_pro
🛠️ Version: 2.0.5
---------------------------------------------------
""")

    asyncio.create_task(schedule_expiry_check())
    print("Auto removal started ...")
    print("Bot is running...")
    
    await idle()
    print("Bot stopped...")


if __name__ == "__main__":
    # Start web server in background thread
    web_thread = Thread(target=run_web_server, daemon=True)
    web_thread.start()
    print("Web server started on port 10000")
    
    # Run bot
    asyncio.get_event_loop().run_until_complete(devggn_boot())
