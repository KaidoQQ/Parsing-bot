import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv 
import sqlite3
import os

load_dotenv("tokens.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
  kb = [
    [KeyboardButton(text = "👨‍⚕️ Doctor Search"),
    KeyboardButton(text = "🛍 Product Search")
    ],
    [
      KeyboardButton(text = "ℹ️ Help")
    ]
  ]

  keyboard = ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder="Select an option"
  )

  await message.answer(
    f"Hello, {message.from_user.first_name}! I am your Parser Bot. Choose an option:",
    reply_markup=keyboard
  )

  

async def main():
  print("Bot Started!")
  await dp.start_polling(bot)

if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print("Bot collapse!")