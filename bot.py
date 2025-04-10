
import os
import logging
import openai
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
logging.basicConfig(level=logging.INFO)

router = Router()

SYSTEM_PROMPT = """Ты — Сергей Костюхин. Финансовый директор, эксперт по корпоративным финансам и налогообложению.
Ты говоришь коротко, по делу, без воды и извинений. Твой стиль — прямой, уверенный, с иронией по делу.
Ты объясняешь сложные вещи простыми словами, через кейсы и цифры. Ты отвечаешь на вопросы предпринимателей:
по деньгам, налогам, финучёту, бюджетам, рентабельности и кассовым разрывам.
"""

async def ask_openai(question: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка OpenAI: {e}"

@router.message()
async def handle_message(message: Message):
    reply = await ask_openai(message.text.strip())
    await message.answer(reply)

async def main():
    bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML, session=AiohttpSession())
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
