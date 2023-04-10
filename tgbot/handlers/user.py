import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from ..config import Settings
from ..dialogs.estimate import states

logger = logging.getLogger(__name__)
user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, dialog_manager: DialogManager, **data):
    config: Settings = data.get("config")
    db_session = data.get("db_session")
    http_session = data.get("http_session")
    http_proxy = data.get("http_proxy")

    await dialog_manager.start(states.ProposalStates.start_window,
                               data={"started_by": message.from_user.mention_html(),},
                               mode=StartMode.RESET_STACK)

