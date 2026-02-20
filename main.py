from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = "ВАШ_ТОКЕН_БОТА"
MANAGER_CHAT_ID = "ID_ЧАТА_МЕНЕДЖЕРА"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Главное меню с услугами
kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.add(KeyboardButton("💇 Стрижка"))
kb_main.add(KeyboardButton("💅 Маникюр"))
kb_main.add(KeyboardButton("💆 Массаж"))
kb_main.add(KeyboardButton("🗓 Другая услуга"))

# Временное хранилище данных
user_data = {}

# Старт
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Привет! Я ваш личный помощник студии красоты ✨\nВыберите услугу:",
        reply_markup=kb_main
    )

# Выбор услуги
@dp.message_handler(lambda message: message.text in ["💇 Стрижка", "💅 Маникюр", "💆 Массаж", "🗓 Другая услуга"])
async def choose_service(message: types.Message):
    user_data[message.from_user.id] = {"service": message.text}
    await message.answer("Введите ваше имя:")

# Ввод имени
@dp.message_handler(lambda message: message.from_user.id in user_data and "name" not in user_data[message.from_user.id])
async def get_name(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    await message.answer("Введите ваш телефон:")

# Ввод телефона
@dp.message_handler(lambda message: message.from_user.id in user_data and "phone" not in user_data[message.from_user.id])
async def get_phone(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.text
    await message.answer("Напишите комментарий или пожелания (если есть), если нет — просто напишите 'нет':")

# Ввод комментария и отправка менеджеру
@dp.message_handler(lambda message: message.from_user.id in user_data and "comment" not in user_data[message.from_user.id])
async def get_comment(message: types.Message):
    user_data[message.from_user.id]["comment"] = message.text
    
    data = user_data[message.from_user.id]
    
    # Отправка заявки менеджеру
    await bot.send_message(
        MANAGER_CHAT_ID,
        f"📌 Новая заявка!\n"
        f"Услуга: {data['service']}\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Комментарий: {data['comment']}"
    )
    
    await message.answer("Спасибо! Ваша заявка принята ✅ Мы скоро свяжемся с вами.")
    del user_data[message.from_user.id]

# Обработка неизвестных сообщений
@dp.message_handler()
async def unknown(message: types.Message):
    await message.answer("Пожалуйста, выберите услугу из меню ниже ⬇", reply_markup=kb_main)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)