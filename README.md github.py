import asyncio
import os
import uuid
import sys

from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest
from telethon.tl import functions
from telethon.errors import UserAlreadyParticipantError, ChatNotModifiedError


# ================== DEMO DEVICE ID (SERVER YO‘Q) ==================

device_id = str(uuid.uuid4())

print("🚀 Demo ishlamoqda (shaxsiy server YO‘Q)")
print("Sizning qurilma ID:", device_id)
print("✅ RUXSAT BOR. DAVOM ETAMIZ...\n")


# ================== SOZLAMALAR ==================

API_ID = 25797876
API_HASH = "21d58c65a68492e2947ab809053cc8e6"
BOT_USERNAME = "tinglabot"
SESSIONS_DIR = "sessions"


# ================== PAPKA ==================

if not os.path.exists(SESSIONS_DIR):
    os.makedirs(SESSIONS_DIR)


# ================== YORDAMCHI ==================

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_sessions():
    return [f.replace('.session', '') for f in os.listdir(SESSIONS_DIR) if f.endswith('.session')]


# ================== AKKAUNT QO‘SHISH ==================

async def add_account():
    clear()
    print("=== AKKAUNT QO‘SHISH ===")
    phone = input("Telefon raqam (+998...): ").strip()
    session_name = phone.replace('+', '').replace(' ', '')
    path = os.path.join(SESSIONS_DIR, session_name)

    client = TelegramClient(path, API_ID, API_HASH)
    await client.start(phone=phone)

    print("✅ Akkaunt muvaffaqiyatli qo‘shildi!")
    await client.disconnect()
    input("Enter bosing...")


# ================== BITTA GURUH ==================

async def create_one_group(client, idx):
    try:
        result = await client(CreateChannelRequest(
            title=f"Guruh {idx}",
            about="Guruh avtomatik yaratildi",
            megagroup=True
        ))
        channel = result.chats[0]

        try:
            await client(functions.channels.TogglePreHistoryHiddenRequest(
                channel=channel,
                enabled=False
            ))
        except ChatNotModifiedError:
            pass

        try:
            bot = await client.get_entity(BOT_USERNAME)
            await client(InviteToChannelRequest(channel=channel, users=[bot]))
        except UserAlreadyParticipantError:
            pass

        await client.send_message(channel, "Xush kelibsiz! Guruh tayyor")
        print(f"✅ Guruh yaratildi: {channel.title}")

    except Exception as e:
        print("❌ Xato:", e)


# ================== AKKAUNT UCHUN ==================

async def groups_for_account(sess, count, delay):
    client = TelegramClient(os.path.join(SESSIONS_DIR, sess), API_ID, API_HASH)
    await client.start()

    for i in range(1, count + 1):
        await create_one_group(client, i)
        if i < count:
            await asyncio.sleep(delay)

    await client.disconnect()


# ================== GURUH YARATISH ==================

async def create_groups():
    clear()
    sessions = get_sessions()

    if not sessions:
        print("❌ Akkaunt yo‘q")
        input("Enter bosing...")
        return

    for i, s in enumerate(sessions, 1):
        print(f"{i}) {s}")
    print(f"{len(sessions)+1}) BARCHASI")

    choice = input("Tanlang: ").strip()

    if choice == str(len(sessions) + 1):
        selected = sessions
    else:
        selected = [sessions[int(choice) - 1]]

    count = int(input("Nechta guruh?: "))
    delay = float(input("Delay (sek): "))

    for s in selected:
        await groups_for_account(s, count, delay)

    print("✅ BARCHA GURUHLAR YARATILDI")
    input("Enter bosing...")


# ================== MENYU ==================

def menu():
    clear()
    print("============================")
    print(" TELEGRAM AUTO TOOL ")
    print("============================")
    print("1. Akkaunt qo‘shish")
    print("2. Faol akkauntlar")
    print("3. Guruh yaratish")
    print("0. Chiqish")


async def main():
    while True:
        menu()
        c = input("Tanlang: ").strip()
        if c == '1':
            await add_account()
        elif c == '2':
            clear()
            print("Faol akkauntlar:")
            for s in get_sessions():
                print("-", s)
            input("Enter bosing...")
        elif c == '3':
            await create_groups()
        elif c == '0':
            break


if __name__ == "__main__":
    asyncio.run(main())
