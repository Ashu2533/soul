import soul
import asyncio
from threading import Thread

def start_bot():
    soul.bot.polling()

bot_thread = Thread(target=start_bot)
bot_thread.start()

loop = asyncio.get_event_loop()
loop.run_until_complete(soul.start_asyncio_loop())