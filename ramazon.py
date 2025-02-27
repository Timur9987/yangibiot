import logging
import requests
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from telethon import TelegramClient

# Bot va Telegram API ma'lumotlari
BOT_TOKEN = "7741320463:AAG3yejtGuSRl-46v00E_TolYpOi5rslizA"
API_ID = 29337025  # my.telegram.org saytidan oling
API_HASH = "19TRkrbLDpFQdfsinsVZBtsguKu2AbZQr2"
CHANNEL_USERNAME = "manguzarmasjidi"

# Aiogram va Telethon klientlarini yaratamiz
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
telethon_client = TelegramClient("session_name", API_ID, API_HASH)

# Oxirgi namoz vaqtlarini olish uchun o'zgaruvchi
latest_prayer_times = "Ma'lumotlar yuklanmoqda..."

# Telegram kanalidan oxirgi namoz vaqtlarini olish
async def fetch_latest_prayer_times():
    global latest_prayer_times
    async with telethon_client:
        async for message in telethon_client.iter_messages(CHANNEL_USERNAME, limit=1):
            latest_prayer_times = message.text
            print("Yangilangan namoz vaqtlari:", latest_prayer_times)

# Qur'on oyatlari va hadislar
OYAT_HADISLAR = [
    "📖 *Qur'on oyati:* 'Albatta, namoz fahsh va munkardan qaytaradi.' (Ankabut, 45)",
    "📖 *Hadis:* 'Sizlarning eng yaxshilaringiz – Qur’onni o‘rganib, uni boshqalarga o‘rgatganlaringizdir.' (Buxoriy)",
]

ZIKRLAR_DUOLAR = [
    "🤲 *Subhanalloh* – 'Allohni pok deb bilaman'",
    "🤲 *Alhamdulillah* – 'Hamd Allohgadir'",
]

# Klaviatura tugmalari
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Bugungi namoz vaqtlari")],
        [KeyboardButton(text="📖 Qur'on oyati / Hadis")],
        [KeyboardButton(text="🤲 Zikr va Duolar")],
    ],
    resize_keyboard=True
)

# Start komandasi
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Assalomu alaykum! Ramazon botiga xush kelibsiz! 🌙\n\n"
                         "Kerakli bo‘limni tanlang:", reply_markup=keyboard)

# Telegram kanalidan eng so‘nggi namoz vaqtlarini olish
@dp.message(lambda message: message.text == "📅 Bugungi namoz vaqtlari")
async def send_prayer_times(message: types.Message):
    await fetch_latest_prayer_times()  # Har safar so‘ralganda yangilash
    await message.answer(latest_prayer_times, parse_mode="Markdown")

# Qur'on oyati yoki hadis yuborish
@dp.message(lambda message: message.text == "📖 Qur'on oyati / Hadis")
async def send_oyat_hadis(message: types.Message):
    await message.answer(random.choice(OYAT_HADISLAR), parse_mode="Markdown")

# Zikr va duolar
@dp.message(lambda message: message.text == "🤲 Zikr va Duolar")
async def send_zikr_duo(message: types.Message):
    await message.answer(random.choice(ZIKRLAR_DUOLAR), parse_mode="Markdown")

# Botni ishga tushirish
async def main():
    await telethon_client.connect()
    await fetch_latest_prayer_times()  # Bot ishga tushganda yangilash
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
