# ---------------------------------------------------
# File Name: __main__.py
# Description: A Pyrogram bot for downloading and uploading Telegram files
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Created: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

import asyncio
import importlib
from pyrogram import idle
from devgagan.modules import ALL_MODULES

# ----------------------------Bot-Start---------------------------- #

loop = asyncio.get_event_loop()

async def devggn_boot():
    for all_module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + all_module)
    print("""
---------------------------------------------------
📂 Bot Deployed successfully ...
👨‍💻 Author: Gagan
🌐 GitHub: https://github.com/devgaganin/
🛠️ Version: 2.0.5
📜 License: MIT License
---------------------------------------------------
""")
    await idle()
    print("Bot stopped...")

if __name__ == "__main__":
    loop.run_until_complete(devggn_boot())

# ------------------------------------------------------------------ #hub.com/devgaganin/
📬 Telegram: https://t.me/team_spy_pro
▶️ YouTube: https://youtube.com/@dev_gagan
🗓️ Created: 2025-01-11
🔄 Last Modified: 2025-01-11
🛠️ Version: 2.0.5
📜 License: MIT License
---------------------------------------------------
""")
    await idle()
    print("Bot stopped...")

if __name__ == "__main__":
    loop.run_until_complete(devggn_boot())

# ------------------------------------------------------------------ #e: https://youtube.com/@dev_gagan
🗓️ Created: 2025-01-11
🔄 Last Modified: 2025-01-11
🛠️ Version: 2.0.5
📜 License: MIT License
---------------------------------------------------
""")

    asyncio.create_task(schedule_expiry_check())
    print("Auto removal started ...")
    await idle()
    print("Bot stopped...")


if __name__ == "__main__":
    loop.run_until_complete(devggn_boot())

# ------------------------------------------------------------------ #
