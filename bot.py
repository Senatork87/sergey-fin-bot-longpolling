import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML, session=AiohttpSession())
dp = Dispatcher()
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@dp.message()
async def handle_message(message: types.Message):
    if not message.text:
        return
    await message.answer("Думаю...")

    try:
        completion = await openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text}],
            temperature=0.7,
        )
        reply_text = completion.choices[0].message.content
        await message.answer(reply_text.strip())
    except Exception as e:
        logging.exception("OpenAI error:")
        await message.answer("Ошибка OpenAI: " + str(e))

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
