import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from asgiref.sync import sync_to_async
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "async.settings")
django.setup()

from core.models import Product

API_TOKEN = "7261511602:AAEMEu3A3F-n3m5dFhl0nRfuTAO9ZTVvpPk"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Mahsulotlar")]
    ],
    resize_keyboard=True
)

@sync_to_async
def get_products():
    return list(Product.objects.values("name", "price"))

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Salom! Quyidagi tugmani bosing", reply_markup=main_menu)

@dp.message(lambda msg: msg.text == "Mahsulotlar")
async def products(message: types.Message):
    products = await get_products()
    if not products:
        await message.answer("Hozircha mahsulot yo‘q")
    else:
        text = "\n".join([f"{p['name']} - {p['price']} so‘m" for p in products])
        await message.answer(text)

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
