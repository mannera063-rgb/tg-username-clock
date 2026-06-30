import os, sys, zipfile, asyncio
from datetime import datetime

# Распаковываем официальную сессию tdata, если её еще нет
if os.path.exists('tdata.zip') and not os.path.exists('tdata'):
if os.path.exists('src/tdata.zip') and not os.path.exists('src/tdata'):
    with zipfile.ZipFile('src/tdata.zip', 'r') as zip_ref:
        zip_ref.extractall('src/tdata')

os.system("pip install opentele")
from opentele.td import TDesktop
from opentele.tl import TelegramClient

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
tdata_path = "src/tdata"
    td = TDesktop(tdata_path)
    client = await td.ToTelethon(session="session_name.session", flag=None)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ Ошибка: Сессия tdata не авторизована!")
        return
        
    print("🚀 Официальные часы успешно запущены в облаке!")
    await update_clock(client)

if __name__ == '__main__':
    from telethon import functions
    asyncio.run(main())
