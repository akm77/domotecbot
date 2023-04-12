import logging
from tempfile import NamedTemporaryFile

from aiogram import Router, F, Bot
from aiogram.types import Message

from tgbot.services.vosk import Transcriber

logger = logging.getLogger(__name__)
sound_router = Router()


@sound_router.message(F.audio | F.voice)
async def sound_to_text(message: Message, bot: Bot, **data):
    stt: Transcriber = data.get("transcriber")
    file_id = message.audio.file_id if message.audio else message.voice.file_id
    with NamedTemporaryFile() as fp:
        await bot.download(file_id,
                           destination=fp)
        stt.process_file(fp.name)
    result = stt.processed_result
    if not result:
        result = "Не удалось распознать сообщение"
    await message.answer(result)

