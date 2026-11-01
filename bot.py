import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в переменных окружения")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WELCOME_TEXT = (
    "💧 <b>Привет! Это Drop Tune Cloud.</b>\n\n"
    "Здесь музыка артистов находит слушателей:\n"
    "🎧 «Мои дропы» — подборка под твои жанры\n"
    "📈 чарты и свежие дропы\n"
    "❤️ лайки, репосты и комментарии под каждым треком\n\n"
    "Ты музыкант? Загружай треки, планируй релизы, включай пресейвы "
    "и собирай альбомы в студии. А официальным артистам выдаём галочку ✅\n\n"
    "Нажми кнопку ниже и заходи 👇"
)

DROP_TUNE_URL = "https://t.me/droptunecloud_bot?startapp=game_heart"
DROP_STUDIO_URL = "https://t.me/droptunestudio_bot?startapp=game_heart"


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎧 DropTuneCloud",
                    url=DROP_TUNE_URL,
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎛 DropStudio",
                    url=DROP_STUDIO_URL,
                )
            ],
        ]
    )


dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        WELCOME_TEXT,
        reply_markup=main_keyboard(),
        disable_web_page_preview=True,
    )


@dp.message(F.text == "/help")
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Команды:\n/start — показать приветствие и кнопки\n/help — эта справка"
    )


async def main() -> None:
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
