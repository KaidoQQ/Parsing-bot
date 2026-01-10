import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv 
import sqlite3
import os
from parsers.doctor_parser import search_doctors_func
from parsers.product_parser import search_products_func
from tech.to_exel import excel_file
from tech.database import DataBase
from aiogram.types import FSInputFile


load_dotenv("tokens.env")

BOT_TOKEN = os.getenv("BOT_TOKEN") #---- Your token here

logging.basicConfig(level=logging.INFO)

db = DataBase('bot_database.db')

bot = Bot(
  token=BOT_TOKEN, 
  default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()

class DoctorSearch(StatesGroup):
  waiting_for_name = State()
  waiting_for_city = State()
  waiting_for_date = State()

class ProductSearch(StatesGroup):
  waiting_for_category = State()
  waiting_for_budget = State()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
  db.add_user(message.from_user.id, message.from_user.username)
  print(f"👤 User {message.from_user.first_name} saved to DB")

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

@dp.message(F.text =="ℹ️ Help")
async def cmd_help(message: types.Message):
  await message.answer("I can help you find open slots for doctors or track product prices.")


@dp.message(F.text == "👨‍⚕️ Doctor Search")
async def doctor_name_search(message: types.Message, state: FSMContext):
  await message.answer("Please enter the *Specialty* (e.g., Dentist):")
  await state.set_state(DoctorSearch.waiting_for_name)

@dp.message(DoctorSearch.waiting_for_name)
async def doctor_name_chosen(message: types.Message, state: FSMContext):
  await state.update_data(doctor_name = message.text)
  await message.answer("Got it. Now please enter the *City* (e.g., Krakow):")
  await state.set_state(DoctorSearch.waiting_for_city)


@dp.message(DoctorSearch.waiting_for_city)
async def doctor_name_chosen(message: types.Message, state: FSMContext):
  await state.update_data(city = message.text)
  await message.answer("Got it. Now please enter the *Date or Period* (e.g., Nearest):")
  await state.set_state(DoctorSearch.waiting_for_date)

@dp.message(DoctorSearch.waiting_for_date)
async def doctor_date_chosen(message: types.Message, state: FSMContext):
  user_data = await state.get_data()
  name = user_data['doctor_name']
  city = user_data['city']
  date = message.text

  search_query = f"Doctor: {name}, City: {city}, Date: {date}"
  db.add_search_log(message.from_user.id, "doctor_search", search_query)

  await message.answer(f"🔎 Searching for *{name}* in *{city}* on *Date[{date}]*... Please wait.")

  result_data = await search_doctors_func(name,date,city)

  file_path = await excel_file(result_data)
  if file_path:
    document = FSInputFile(file_path,filename=f"{name}_doctor_list.xlsx")
    await message.answer_document(document, caption=f"✅ Done! Here is the list for you")
  else:
    await message.answer("❌ [ERROR] Nothing was found or error creating file.")
  await state.clear()

@dp.message(F.text == "🛍 Product Search")
async def product_category_search(message: types.Message, state:FSMContext):
  await message.answer("Please enter the *Product Category* or *Name* (e.g., iPhone 15, Sneakers):")
  await state.set_state(ProductSearch.waiting_for_category)

@dp.message(ProductSearch.waiting_for_category)
async def product_category_chosen(message: types.Message, state:FSMContext):
  await state.update_data(category = message.text)
  await message.answer("Okay. What is your *Budget*? (e.g., 1000 USD):")
  await state.set_state(ProductSearch.waiting_for_budget)

@dp.message(ProductSearch.waiting_for_budget)
async def product_budget_chosen(message: types.Message, state: FSMContext):
  user_data = await state.get_data()
  category = user_data['category']
  budget = message.text

  search_query = f"Category: {category}, Budget: {budget}"
  db.add_search_log(message.from_user.id, "product_search", search_query)

  await message.answer(f"🔎 Searching for *{category}* with budget *{budget}*... Please wait.")

  result_data = await search_products_func(category,budget)
  file_path = await excel_file(result_data)
  if file_path:
    document = FSInputFile(file_path)
    await message.answer_document(document, caption=f"✅ Done! Here is the list for you")
  else:
    await message.answer("❌ [ERROR] Nothing was found or error creating file.")
  await state.clear()


async def main():
  print("🧿Bot Started!")
  await dp.start_polling(bot)

if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print("☠️Bot collapse!")