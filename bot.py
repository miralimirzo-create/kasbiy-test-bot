import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart


TOKEN = os.getenv "8287939968:AAHwXfaBdnxbCYaKII5XPUETDkHxwlmdABg"

bot = Bot(token=TOKEN)
dp = Dispatcher()

questions = [
    {
        "question": "O‘zbekiston Respublikasi Konstitutsiyasining yangi tahriri qachon qabul qilingan?",
        "options": [
            "2022-yil 30-aprel",
            "2023-yil 30-aprel",
            "2021-yil 1-may",
            "2020-yil 29-sentyabr"
        ],
        "correct": "2023-yil 30-aprel"
    },
    {
        "question": "Konstitutsiya nechta moddadan iborat?",
        "options": [
            "120 modda",
            "155 modda",
            "180 modda",
            "200 modda"
        ],
        "correct": "155 modda"
    },
    {
        "question": "Bilim olish huquqi Konstitutsiyaning nechanchi moddasida belgilangan?",
        "options": [
            "45-modda",
            "50-modda",
            "52-modda",
            "60-modda"
        ],
        "correct": "50-modda"
    },
    {
        "question": "Yangi Ta’lim to‘g‘risidagi qonun qachon qabul qilingan?",
        "options": [
            "2019-yil",
            "2020-yil 29-sentyabr",
            "2021-yil",
            "2022-yil"
        ],
        "correct": "2020-yil 29-sentyabr"
    },
    {
        "question": "Professional ta’lim nechta darajadan iborat?",
        "options": [
            "2 ta",
            "3 ta",
            "4 ta",
            "5 ta"
        ],
        "correct": "3 ta"
    }
]

user_data = {}

@dp.message(CommandStart())
async def start_test(message: types.Message):
    user_data[message.from_user.id] = {"current": 0, "score": 0}
    await send_question(message)

async def send_question(message):
    user_id = message.from_user.id
    current = user_data[user_id]["current"]

    if current >= len(questions):
        score = user_data[user_id]["score"]
        await message.answer(f"✅ Test tugadi!\nNatija: {score}/{len(questions)}")
        return

    q = questions[current]

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in q["options"]],
        resize_keyboard=True
    )

    await message.answer(q["question"], reply_markup=keyboard)

@dp.message()
async def check_answer(message: types.Message):
    user_id = message.from_user.id

    # Agar foydalanuvchi test boshlamagan bo‘lsa
    if user_id not in user_data:
        await message.answer("Testni boshlash uchun /start bosing")
        return

    current = user_data[user_id]["current"]

    # Agar savollar tugagan bo‘lsa
    if current >= len(questions):
        await message.answer("Test tugagan. Qayta boshlash uchun /start bosing")
        return

    correct_answer = questions[current]["correct"]

    if message.text == correct_answer:
        user_data[user_id]["score"] += 1
        await message.answer("✅ To‘g‘ri!")
    else:
        await message.answer(f"❌ Noto‘g‘ri!\nTo‘g‘ri javob: {correct_answer}")

    user_data[user_id]["current"] += 1

    # Keyingi savolni yuborish
    if user_data[user_id]["current"] < len(questions):
        await send_question(message)
    else:
        score = user_data[user_id]["score"]
        await message.answer(f"✅ Test tugadi!\nNatija: {score}/{len(questions)}")

async def main():
    print("🚀 BOT ISHLAYAPTI...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())