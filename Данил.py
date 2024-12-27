from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Создаем бота
bot = Bot(token='8026739943:AAGdNaTZFtX43nkfZiCTvy2VgeHHZukvSbM')
dp = Dispatcher(bot)

# Создаем клавиатуру для главного меню
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('🔧 Услуги'))
    keyboard.add(KeyboardButton('📝 Записаться'))
    keyboard.add(KeyboardButton('ℹ️ О нас'), KeyboardButton('📞 Контакты'))
    return keyboard

# Создаем клавиатуру для услуг
def get_services_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton('Диагностика', callback_data='service_diagnostic'),
        InlineKeyboardButton('Ремонт двигателя', callback_data='service_engine'),
        InlineKeyboardButton('Замена масла', callback_data='service_oil'),
        InlineKeyboardButton('Ремонт ходовой', callback_data='service_suspension'),
        InlineKeyboardButton('Назад', callback_data='back_to_main')
    )
    return keyboard

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в AutoService Bot!\n"
        "Выберите интересующий вас раздел:",
        reply_markup=get_main_keyboard()
    )

# Обработчик кнопки "Услуги"
@dp.message_handler(lambda message: message.text == "🔧 Услуги")
async def show_services(message: types.Message):
    await message.answer(
        "Выберите интересующую вас услугу:",
        reply_markup=get_services_keyboard()
    )

# Обработчик кнопки "О нас"
@dp.message_handler(lambda message: message.text == "ℹ️ О нас")
async def about_us(message: types.Message):
    await message.answer(
        "🏢 Наш автосервис работает с 2010 года.\n"
        "✅ Мы предоставляем полный спектр услуг по ремонту и обслуживанию автомобилей.\n"
        "👨‍🔧 У нас работают только квалифицированные специалисты.\n"
        "⚡️ Гарантия на все виды работ."
    )

# Обработчик кнопки "Контакты"
@dp.message_handler(lambda message: message.text == "📞 Контакты")
async def contacts(message: types.Message):
    await message.answer(
        "📍 Адрес: ул. Примерная, 123\n"
        "📱 Телефон: +7 (999) 123-45-67\n"
        "🕐 Режим работы: ПН-ВС 9:00-21:00\n"
        "📧 Email: info@autoservice.com"
    )

# Обработчик кнопки "Записаться"
@dp.message_handler(lambda message: message.text == "📝 Записаться")
async def book_service(message: types.Message):
    await message.answer(
        "Для записи на обслуживание, пожалуйста, оставьте заявку:\n"
        "1. Напишите ваше имя\n"
        "2. Укажите марку и модель автомобиля\n"
        "3. Опишите проблему\n"
        "4. Укажите удобное время\n\n"
        "Наш менеджер свяжется с вами в ближайшее время!"
    )

# Обработчик callback-кнопок услуг
@dp.callback_query_handler(lambda c: c.data.startswith('service_'))
async def process_service_callback(callback_query: types.CallbackQuery):
    service_info = {
        'service_diagnostic': {
            'name': 'Диагностика',
            'description': 'Полная компьютерная диагностика автомобиля',
            'price': 'от 1000 ₽'
        },
        'service_engine': {
            'name': 'Ремонт двигателя',
            'description': 'Капитальный ремонт двигателя любой сложности',
            'price': 'от 15000 ₽'
        },
        'service_oil': {
            'name': 'Замена масла',
            'description': 'Замена масла и фильтров',
            'price': 'от 800 ₽'
        },
        'service_suspension': {
            'name': 'Ремонт ходовой',
            'description': 'Диагностика и ремонт подвески',
            'price': 'от 2000 ₽'
        }
    }
    
    service = service_info.get(callback_query.data)
    if service:
        await callback_query.message.edit_text(
            f"📌 {service['name']}\n"
            f"📝 {service['description']}\n"
            f"💰 Стоимость: {service['price']}\n\n"
            "Для записи нажмите кнопку 'Записаться' в главном меню",
            reply_markup=get_services_keyboard()
        )

# Обработчик кнопки "Назад"
@dp.callback_query_handler(lambda c: c.data == 'back_to_main')
async def process_back_callback(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Выберите интересующий вас раздел:",
        reply_markup=get_main_keyboard()
    )

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)