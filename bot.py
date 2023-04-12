import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog.widgets.text import setup_jinja

from tgbot.config import settings
from tgbot.dialogs import setup_dialogs
from tgbot.handlers.admin import admin_router
from tgbot.handlers.sound_to_text import sound_router
from tgbot.handlers.user import user_router
from tgbot.middlewares.config import ConfigMiddleware, UserDBMiddleware
from tgbot.models.base import create_db_session
from tgbot.services import broadcaster
from tgbot.services.vosk import Transcriber
from tgbot.utils.decimals import formatvalue

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Bot started")


def register_global_middlewares(dp: Dispatcher, config, db_session, transcriber: Transcriber):
    dp.my_chat_member.outer_middleware(ConfigMiddleware(config, db_session, transcriber))
    dp.message.outer_middleware(ConfigMiddleware(config, db_session, transcriber))
    dp.message.outer_middleware(UserDBMiddleware())
    dp.callback_query.outer_middleware(ConfigMiddleware(config, db_session, transcriber))
    dp.callback_query.outer_middleware(UserDBMiddleware())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    config = settings
    if config.use_redis:
        storage = RedisStorage.from_url(config.redis_dsn, key_builder=DefaultKeyBuilder(with_bot_id=True,
                                                                                        with_destiny=True))
    else:
        storage = MemoryStorage()

    db_session = await create_db_session(config.db_dialect, config.db_name, config.db_user,
                                         config.db_pass.get_secret_value(), config.db_host, config.db_echo)
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    setup_jinja(bot=bot, filters={"formatvalue": formatvalue}, enable_async=True)
    setup_dialogs(dp)

    for router in [
        admin_router,
        user_router,
        sound_router
    ]:
        dp.include_router(router)
    stt = Transcriber(model_name=config.vosk_model, lang=config.vosk_language)
    register_global_middlewares(dp, config, db_session, stt)
    await on_startup(bot, config.admins)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
