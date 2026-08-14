import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Сиздин Telegram API Токениңиз
API_TOKEN = '8193831286:AAG-9HLpx3O1q4w5CvczFQkBIOhepIhx9eI'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Башкы меню
def get_main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_2026 = InlineKeyboardButton(text="🔥 Жаңы 2026 ырлар", callback_data="category_2026")
    btn_video = InlineKeyboardButton(text="🎬 Клиптер / Видеолор", callback_data="category_video")
    btn_sub = InlineKeyboardButton(text="💳 Премиум жазылуу (Тарифтер)", callback_data="tariffs")
    keyboard.add(btn_2026, btn_video)
    keyboard.add(btn_sub)
    return keyboard

# Тарифтер менюсу
def get_tariff_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="🎵 Базалык мүмкүндүк — 230 сом", callback_data="pay_230")
    btn2 = InlineKeyboardButton(text="🔥 VIP ТОП 2026 + Видеолор — 350 сом", callback_data="pay_350")
    btn3 = InlineKeyboardButton(text="👑 Безлимит (Музыка + Видео) — 500 сом", callback_data="pay_500")
    btn_back = InlineKeyboardButton(text="⬅️ Артка кайтуу", callback_data="back_to_main")
    keyboard.add(btn1, btn2, btn3, btn_back)
    return keyboard

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    text = (
        f"Салам, {message.from_user.first_name}!\n\n"
        "🎧 **Музыкалык ботко кош келиңиз!**\n\n"
        "• Жаңы 2026-жылдын хиттерин жана видеолорду көрүү үчүн атайын баскычтарды басыңыз.\n"
        "• Эски ырларды табуу үчүн жөн гана **ырдын же ырчынын атын жазып жөнөтүңүз**."
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=get_main_menu())

@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.Callback_query):
    code = callback_query.data

    if code == "tariffs":
        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text="💳 **Премиум тарифти тандаңыз:**\n\nТөлөм жүргүзгөндөн кийин эксклюзивдүү 2026-жылдын ырларына жана видеолоруна мүмкүндүк аласыз.",
            parse_mode="Markdown",
            reply_markup=get_tariff_menu()
        )
    elif code in ["pay_230", "pay_350", "pay_500"]:
        price = code.split('_')[1]
        await bot.send_message(
            callback_query.from_user.id,
            f"✅ Сиз **{price} сомдук** тарифти тандадыңыз.\n\n"
            "Төлөмдү MBank же О!Деньги аркылуу которуңуз:\n📱 **+996 XXX XX XX XX**\n\n"
            "Төлөгөндөн кийин чекти админге жөнөтүңүз."
        )
    elif code == "category_2026":
        await bot.send_message(
            callback_query.from_user.id,
            "🔥 **2026-жылдын жаңы ырлары** даяр. Жүктөө үчүн **Премиум жазылууну** тандаңыз!",
            reply_markup=get_tariff_menu()
        )
    elif code == "back_to_main":
        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text="Башкы менюга кайттыңыз:",
            reply_markup=get_main_menu()
        )

@dp.message_handler(content_types=['text'])
async def search_old_songs(message: types.Message):
    song_name = message.text
    await message.answer(f"🔍 **'{song_name}'** эски ырлардын арасынан изделүүдө...")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
