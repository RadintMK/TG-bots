from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = "7688802821:AAGCvBH__yDJi6t3PSpXJvBAR_fswo8w_fA"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Записаться"), KeyboardButton("Отмена")
)

specialization_menu = ReplyKeyboardMarkup(resize_keyboard=True)
specialization_menu.add(KeyboardButton("Терапевт"))
specialization_menu.add(KeyboardButton("Стоматолог"))
specialization_menu.add(KeyboardButton("Хирург"))
specialization_menu.add(KeyboardButton("Педиатр"))
specialization_menu.add(KeyboardButton("Отмена"))

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Добро пожаловать! Я бот для записи ко врачам. Выберите действие:",
        reply_markup=main_menu,
    )

@dp.message_handler(lambda message: message.text == "Записаться")
async def ask_name(message: types.Message):
    user_data[message.from_user.id] = {}  
    await message.answer("Как вас зовут?")
    user_data[message.from_user.id]["step"] = "name"

@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get("step") == "name")
async def choose_specialization(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    await message.answer(
        "Какого врача вы хотите выбрать?",
        reply_markup=specialization_menu
    )
    user_data[message.from_user.id]["step"] = "specialization"

@dp.message_handler(lambda message: message.text in ["Терапевт", "Стоматолог", "Хирург", "Педиатр"])
async def ask_date(message: types.Message):
    user_data[message.from_user.id]["specialization"] = message.text
    await message.answer("Укажите дату приёма (в формате ДД.ММ.ГГГГ)")
    user_data[message.from_user.id]["step"] = "date"

@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get("step") == "date")
async def ask_time(message: types.Message):
    user_data[message.from_user.id]["date"] = message.text
    await message.answer("Укажите время приёма (в формате ЧЧ:ММ)")
    user_data[message.from_user.id]["step"] = "time"

@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get("step") == "time")
async def confirm_data(message: types.Message):
    user_data[message.from_user.id]["time"] = message.text
    user = user_data[message.from_user.id]
    await message.answer(
        f"Проверьте данные:\n"
        f"Имя: {user['name']}\n"
        f"Врач: {user['specialization']}\n"
        f"Дата: {user['date']}\n"
        f"Время: {user['time']}\n\n"
        f"Спасибо за запись! Для новой записи нажмите /start.",
        reply_markup=main_menu,
    )
    user_data.pop(message.from_user.id)

@dp.message_handler(lambda message: message.text == "Отмена")
async def cancel(message: types.Message):
    user_data.pop(message.from_user.id, None)
    await message.answer("Действие отменено. Для начала нажмите /start.", reply_markup=main_menu)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True) 