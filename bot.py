import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    FSInputFile  # Нужен для отправки локальных картинок
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

# --- ССЫЛКИ ---
DROP_TUNE_URL = "https://t.me/droptunecloud_bot?startapp=game_heart"
DROP_STUDIO_URL = "https://t.me/droptunestudio_bot?startapp=game_heart"
DROP_CHANNEL_URL = "https://t.me/droptunecloud" # ЗАМЕНИТЕ НА ССЫЛКУ ВАШЕГО КАНАЛА!

def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎧 DropTuneCloud", url=DROP_TUNE_URL)],
            [InlineKeyboardButton(text="🎛 DropStudio", url=DROP_STUDIO_URL)],
            [InlineKeyboardButton(text="📢 Drop Channel", url=DROP_CHANNEL_URL)],
        ]
    )

dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    # Путь к картинке (файл должен лежать рядом с bot.py)
    photo_path = "welcome.jpg" 
    
    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo=photo,
            caption=WELCOME_TEXT,
            reply_markup=main_keyboard(),
            parse_mode=ParseMode.HTML
        )
    else:
        # Если картинку забыли добавить в репозиторий, бот пришлет хотя бы текст
        logger.warning(f"Файл {photo_path} не найден! Отправляю только текст.")
        await message.answer(
            WELCOME_TEXT,
            reply_markup=main_keyboard(),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
        )

@dp.message(F.text == "/help")
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Команды:\n/start — показать приветствие и кнопки\n/help — эта справка"
    )

# --- Фейковый веб-сервер для Render (чтобы не было ошибки "No open ports") ---
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Фейковый веб-сервер запущен на порту {port}")

async def main() -> None:
    # Запускаем фейковый веб-сервер параллельно с ботом
    asyncio.create_task(start_web_server())
    
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    logger.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
