import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

def menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="🎁 NFT Gifts", callback_data="gifts")
    kb.button(text="⭐ Telegram Stars", callback_data="stars")
    kb.button(text="💎 Telegram Premium", callback_data="premium")
    kb.button(text="👤 Аренда юзернеймов", callback_data="usernames")
    kb.button(text="📋 Мои заявки", callback_data="orders")
    kb.button(text="🆘 Поддержка", callback_data="support")
    kb.adjust(2, 2, 1, 1)
    return kb.as_markup()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "✨ PRESTIGE MARKET\n\n"
        "Добро пожаловать в цифровой маркетплейс!\n"
        "Выберите интересующий раздел:",
        reply_markup=menu()
    )

@dp.callback_query(F.data.in_(
    ["gifts", "stars", "premium", "usernames", "orders", "support"]
))
async def sections(callback: CallbackQuery):
    texts = {
        "gifts": "🎁 NFT GIFTS\n\nКаталог подарков скоро будет доступен.",
        "stars": "⭐ TELEGRAM STARS\n\nРаздел заказов Stars.",
        "premium": "💎 TELEGRAM PREMIUM\n\nРаздел подписок Premium.",
        "usernames": "👤 USERNAMES\n\nРаздел аренды юзернеймов.",
        "orders": "📋 МОИ ЗАЯВКИ\n\nВаши заявки появятся здесь.",
        "support": "🆘 ПОДДЕРЖКА\n\nНапишите администратору: @PrestigeMarketShopBot"
    }

    await callback.message.edit_text(
        texts[callback.data],
        reply_markup=menu()
    )
    await callback.answer()

@dp.message()
async def other_messages(message: Message):
    await message.answer("Используйте меню бота командой /start.")

async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN не задан в Secrets")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
