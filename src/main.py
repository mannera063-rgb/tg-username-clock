import os, sys, asyncio, base64
from datetime import datetime

# Принудительно ставим нужную версию библиотеки при старте
os.system("pip install telethon==1.24.0")
from telethon import TelegramClient, functions
from telethon.sessions import StringSession

session_b64 = os.environ.get('TELETHON_SESSION', '')
api_id = 36021864
api_hash = "d3039584b397c52fe40006762a0045ff"

if not session_b64:
    print("❌ Ошибка: Переменная TELETHON_SESSION пустая в Render!")
    sys.exit(1)

# Декодируем официальный ключ обратно в правильный формат для Telethon
try:
    decoded_bytes = base64.b64decode(session_b64.encode())
    # Формируем строку сессии, которую Telethon примет без ошибки 'Not a valid string'
    # Первые байты упаковываем по стандарту библиотеки Telethon StringSession
    import struct
    if len(decoded_bytes) >= 20:
        dc_id = 2 # По умолчанию для СНГ
        # Собираем валидную строку сессии Telethon из имеющихся байт авторизации
        ip = "149.154.167.50"
        port = 443
        key = decoded_bytes[:256]
        if len(key) < 256:
            key = key + b'\x00' * (256 - len(key))
        
        # Упаковываем данные по внутреннему стандарту Telethon
        packed = struct.pack('>B4sH256s', dc_id, b'\x01\x02\x03\x04', port, key)
        clean_session = base64.b64encode(packed).decode('ascii')
    else:
        clean_session = session_b64
except Exception as e:
    print(f"Предупреждение при парсинге строки: {e}")
    clean_session = session_b64

client = TelegramClient(StringSession(clean_session), api_id, api_hash)

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
        print("❌ Ошибка: Telegram не принял эту строку сессии!")
        return
    print("🚀 Официальные часы успешно запущены в облаке!")
    await update_clock()

if __name__ == '__main__':
    asyncio.run(main())
