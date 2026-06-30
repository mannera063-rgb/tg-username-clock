import os, sys, asyncio, base64
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import StringSession

session_str = os.environ.get('TELETHON_SESSION', '')
api_id = 36021864
api_hash = "d3039584b397c52fe40006762a0045ff"

if not session_str:
    print("❌ Ошибка: Переменная TELETHON_SESSION пустая в настройках Render!")
    sys.exit(1)

# Раскодируем нашу строку обратно в имя сессии
session_name = base64.b64decode(session_str.encode()).decode()
client = TelegramClient(f'src/{session_name}.session', api_id, api_hash)

async def update_clock():
    while True:
        try:
            current_time = datetime.now().strftime("<%H:%M>")
            await client(functions.account.UpdateProfileRequest(last_name=current_time))
            print(f"⏰ Время успешно обновлено: {current_time}")
        except Exception as e:
            print(f"Ошибка обновления: {e}")
        await asyncio.sleep(60)

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        print("❌ Ошибка: Файл сессии не авторизован сервером Telegram!")
        return
    print("🚀 Официальные часы успешно запущены в облаке!")
    await update_clock()

if __name__ == '__main__':
    from telethon import functions
    asyncio.run(main())
