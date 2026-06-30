import os, sys, asyncio
from datetime import datetime

print("--- СТАРТ СКРИПТА В ОБЛАКЕ ---")

# Проверяем, где лежат файлы официального Телеграма
# Если они лежат прямо в src, opentele их прочитает из текущей папки '.'
os.system("pip install opentele==1.1.1 telethon==1.24.0 PyQt5-sip")

from opentele.td import TDesktop
from telethon import TelegramClient

async def update_clock(client):
    while True:
        try:
            current_time = datetime.now().strftime("<%H:%M>")
            await client(functions.account.UpdateProfileRequest(last_name=current_time))
            print(f"⏰ Время успешно обновлено: {current_time}")
        except Exception as e:
            print(f"Ошибка обновления: {e}")
        await asyncio.sleep(60)

async def main():
    try:
        # Инициализируем сессию напрямую из распакованных файлов в папке src
        td = TDesktop(".")
        client = await td.ToTelethon(session="session_name.session", flag=None)
        await client.connect()
        
        if not await client.is_user_authorized():
            print("❌ Ошибка: Официальная сессия не авторизована!")
            return
            
        print("🚀 Официальные часы успешно запущены в облаке!")
        await update_clock(client)
    except Exception as e:
        print(f"Критическая ошибка запуска: {e}")

if __name__ == '__main__':
    from telethon import functions
    asyncio.run(main())
