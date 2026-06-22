import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, WebAppData
from config import BOT_TOKEN, TMA_URL, ADMIN_ID

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

# ============================================================
# КЛАВИАТУРЫ
# ============================================================
def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍 Открыть магазин", web_app=WebAppInfo(url=TMA_URL))],
            [KeyboardButton(text="📦 Мои заказы"), KeyboardButton(text="💬 Поддержка")],
        ],
        resize_keyboard=True
    )

# ============================================================
# ХЕНДЛЕРЫ
# ============================================================
@dp.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        f"❄️ <b>Alaska Bots Market</b>\n\n"
        f"💰 Цены от 390₽\n"
        f"⚡ Разработка за 1-3 дня\n"
        f"🎁 Промокод <b>ALASKA40</b> = −40%\n\n"
        f"Нажми кнопку ниже 👇"
    )
    await message.answer(text, reply_markup=main_keyboard(), parse_mode="HTML")

@dp.message(F.web_app_data)
async def process_webapp_data(message: Message, web_app_data: WebAppData):
    try:
        data = json.loads(web_app_data.data)
        order_id = data.get('id', 'unknown')
        product = data.get('product', 'Сборка')
        wishes = data.get('wishes', '')
        contact = data.get('contact', '')
        name = data.get('name', '')
        price = data.get('price', 0)
        promo = data.get('promo', '')

        admin_text = (
            f"🆕 <b>НОВАЯ ЗАЯВКА #{order_id}</b>\n\n"
            f"👤 <b>{name}</b>\n"
            f"📞 {contact}\n"
            f"🛍 <b>{product}</b>\n"
            f"💰 {price}₽\n"
            f"🎟 Промокод: {promo or 'нет'}\n\n"
            f"💬 <b>Пожелания:</b>\n{wishes}"
        )
        await message.bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")

        promo_text = f"\n\n🎁 Промокод {promo} применён! Скидка 40%" if promo == "ALASKA40" else ""
        await message.answer(
            f"✅ <b>Заявка #{order_id} принята!</b>\n\n"
            f"Я свяжусь с вами в течение 1-2 часов.{promo_text}",
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer("❌ Ошибка. Напишите в поддержку.")
        logging.error(f"Error processing webapp data: {e}")

@dp.message(F.text == "📦 Мои заказы")
async def my_orders(message: Message):
    await message.answer(
        "📦 <b>Ваши заказы</b>\n\n"
        "Откройте магазин — там все заказы.",
        parse_mode="HTML"
    )

@dp.message(F.text == "💬 Поддержка")
async def support(message: Message):
    await message.answer(
        "💬 <b>Поддержка</b>\n\n"
        "Напишите вопрос — отвечу в течение часа.",
        parse_mode="HTML"
    )

# ============================================================
# ЗАПУСК
# ============================================================
async def main():
    bot = Bot(token=BOT_TOKEN)
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())