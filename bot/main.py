import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, WebAppData
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector
from config import BOT_TOKEN, TMA_URL, ADMIN_ID

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

# ============================================================
# ПРОКСИ НАСТРОЙКА
# ============================================================
# Замени на свой прокси (формат: socks5://[user:pass@]host:port)
PROXY_URL = 'socks5://185.231.232.11:1080'  # Бесплатный прокси (может не работать)

async def create_bot():
    """Создает бота с прокси"""
    try:
        connector = ProxyConnector.from_url(PROXY_URL)
        session = AiohttpSession(connector=connector)
        bot = Bot(token=BOT_TOKEN, session=session)
        logging.info(f"✅ Бот создан с прокси: {PROXY_URL}")
        return bot
    except Exception as e:
        logging.error(f"❌ Ошибка создания бота с прокси: {e}")
        logging.info("⚠️ Пробую без прокси...")
        return Bot(token=BOT_TOKEN)

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
    bot = await create_bot()
    print("✅ Бот запущен!")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ Критическая ошибка: {e}")
        print("\n💡 Возможные решения:")
        print("1. Проверь прокси - может быть нерабочим")
        print("2. Попробуй другой прокси")
        print("3. Купи прокси на proxy-seller.com")
        print("4. Используй VPS за рубежом")

if __name__ == "__main__":
    asyncio.run(main())