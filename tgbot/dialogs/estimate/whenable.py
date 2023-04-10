from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable

from . import constants


def is_multi_floor(data: Dict, widget: Whenable, manager: DialogManager):
    dialog_data = data.get("dialog_data")
    number_floors = dialog_data.get("number_floors") or 0
    return int(number_floors) > 1


def is_primorsky_region(data: Dict, widget: Whenable, manager: DialogManager):
    estimate_type = manager.find(constants.ProposalForm.PRIMORSKY_REGION)
    return estimate_type.is_checked()
