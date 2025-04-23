from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

API_TOKEN = '7475525184:AAEGJ0HjUL9TarHqcVvGyWt87A7Aif_4Pk4'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("💸 Заработать", callback_data="earn"))
    return keyboard

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"coins": 0}
    coins = user_data[user_id]["coins"]
    await message.answer(
        f"👋 Добро пожаловать в JaloGritoCoin!\nУ тебя {coins} 🪙.",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data == "earn")
async def process_earn(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"coins": 0}
    user_data[user_id]["coins"] += 1
    coins = user_data[user_id]["coins"]
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=f"💸 Ты нажал! У тебя {coins} 🪙.",
        reply_markup=get_main_keyboard()
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

