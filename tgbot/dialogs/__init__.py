from aiogram import Dispatcher
from aiogram_dialog import DialogRegistry

from . import estimate


def setup_dialogs(dp: Dispatcher):
    registry = DialogRegistry()
    for dialog in [
        *estimate.estimate_dialogs(),
    ]:
        registry.register(dialog)  # register a dialog

    registry.setup_dp(dp)
