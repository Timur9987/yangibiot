
import logging
import requests
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# Bot tokenini shu yerga qo‘ying
TOKEN = "7741320463:AAG3yejtGuSRl-46v00E_TolYpOi5rslizA"

# Bot va dispatcher yaratamiz
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Qur'on oyatlari, hadislar, zikr va duolar
OYAT_HADISLAR = [
    "📖 *Qur'on oyati:* 'Albatta, namoz fahsh va munkardan qaytaradi.' (Ankabut, 45)",
    "📖 *Hadis:* 'Sizlarning eng yaxshilaringiz – Qur’onni o‘rganib, uni boshqalarga o‘rgatganlaringizdir.' (Buxoriy)",
    "📖 *Qur'on oyati:* 'Ey, imon keltirganlar! Ro‘za sizlardan oldingi ummatlarga farz qilingani kabi sizga ham farz qilindi.' (Baqara, 183)",
    "📖 *Qur'on oyati:* 'Kim Allohga tavakkal qilsa, U unga kifoya qiladi.' (Taloq, 3)",
    "📖 *Hadis:* 'Kim Ramazon oyida ro‘za tutsa, uning oldingi gunohlari kechiriladi.' (Buxoriy, Muslim)",
]

ZIKRLAR_DUOLAR = [
    "🤲 *Subhanalloh* – 'Allohni pok deb bilaman'",
    "🤲 *Alhamdulillah* – 'Hamd Allohgadir'",
    "🤲 *Allohu Akbar* – 'Alloh buyukdir'",
    "🤲 *La ilaha illalloh* – 'Allohdan o‘zga iloh yo‘q'",
    "🤲 *Astaghfirulloh* – 'Allohdan kechirim so‘rayman'",
]

# Klaviatura tugmalari
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Bugungi namoz vaqtlari (Termiz)")],
        [KeyboardButton(text="🌙 Ramazon taqvimi")],
        [KeyboardButton(text="📖 Qur'on oyati / Hadis")],
        [KeyboardButton(text="🤲 Zikr va Duolar")],
    ],
    resize_keyboard=True
)

# Namoz vaqtlari API
def get_prayer_times(city="Termiz"):
    url = f"https://api.aladhan.com/v1/timingsByCity?city={city}&country=Uzbekistan&method=2"
    response = requests.get(url).json()
    timings = response["data"]["timings"]
    return timings

# Start komandasi
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Assalomu alaykum! Ramazon botiga xush kelibsiz! 🌙\n\n"
                         "Kerakli bo‘limni tanlang:", reply_markup=keyboard)

# Namoz vaqtlari bo‘yicha javob
@dp.message(lambda message: message.text == "📅 Bugungi namoz vaqtlari (Termiz)")
async def send_prayer_times(message: types.Message):
    times = get_prayer_times("Termiz")
    response_text = (f"📅 *Bugungi namoz vaqtlari (Termiz):*\n"
                     f"🌅 *Bomdod:* {times['Fajr']}\n"
                     f"☀ *Quyosh chiqishi:* {times['Sunrise']}\n"
                     f"🌇 *Peshin:* {times['Dhuhr']}\n"
                     f"🌆 *Asr:* {times['Asr']}\n"
                     f"🌃 *Shom:* {times['Maghrib']}\n"
                     f"🌌 *Xufton:* {times['Isha']}")
    await message.answer(response_text, parse_mode="Markdown")

# Qur'on oyati yoki hadis
@dp.message(lambda message: message.text == "📖 Qur'on oyati / Hadis")
async def send_oyat_hadis(message: types.Message):
    await message.answer(random.choice(OYAT_HADISLAR), parse_mode="Markdown")

# Zikr va duolar
@dp.message(lambda message: message.text == "🤲 Zikr va Duolar")
async def send_zikr_duo(message: types.Message):
    await message.answer(random.choice(ZIKRLAR_DUOLAR), parse_mode="Markdown")

# Botni ishga tushirish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
