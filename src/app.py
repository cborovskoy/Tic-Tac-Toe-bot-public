import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import load_config
from src.handlers import game, commands

logging.basicConfig(level=logging.ERROR)


async def main():
    config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp.include_routers(game.router, commands.router)

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.send_message(chat_id=config.tg_bot.admin_ids[-1], text='Bot was started!')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
