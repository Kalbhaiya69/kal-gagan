import asyncio
import importlib
import gc
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import idle
from devgagan import restrict_bot
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Bot Running!')
    
    def log_message(self, format, *args):
        pass


def run_web():
    server = HTTPServer(('0.0.0.0', 10000), Handler)
    server.serve_forever()


async def schedule_expiry_check():
    while True:
        try:
            await check_and_remove_expired_users()
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(3600)
        gc.collect()


async def devggn_boot():
    await restrict_bot()
    
    for all_module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + all_module)
    
    print("Bot Deployed Successfully!")
    asyncio.create_task(schedule_expiry_check())
    print("Auto removal started ...")
    
    await idle()


if __name__ == "__main__":
    Thread(target=run_web, daemon=True).start()
    print("Port 10000 Ready")
    asyncio.get_event_loop().run_until_complete(devggn_boot())
