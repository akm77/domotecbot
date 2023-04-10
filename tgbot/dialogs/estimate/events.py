from aiogram.types import Message
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.common import ManagedWidget
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select, ManagedCheckboxAdapter

from . import states, constants
from ...utils.calculator import CalcParser, CalcLexer
from ...utils.decimals import format_decimal


async def on_number_floors_changed(event: ChatEvent, widget: ManagedWidget[Select], manager: DialogManager, item_id):
    ctx = manager.current_context()
    ctx.dialog_data.update(number_floors=item_id)
    if item_id == '':
        return
    if int(item_id) < 2:
        ctx.dialog_data.update(intermediate_floor_panel_type=0)
        ctx.dialog_data.pop("intermediate_floor_panel_type")


async def on_estimate_type_changed(event: ChatEvent, widget: ManagedWidget[Select], manager: DialogManager, item_id):
    ctx = manager.current_context()
    ctx.dialog_data.update(estimate_type=item_id)


async def on_foundation_type_changed(event: ChatEvent, widget: ManagedWidget[Select], manager: DialogManager, item_id):
    ctx = manager.current_context()
    ctx.dialog_data.update(foundation_type=item_id)


async def on_roof_type_changed(event: ChatEvent, widget: ManagedWidget[Select], manager: DialogManager, item_id):
    ctx = manager.current_context()
    ctx.dialog_data.update(roof_type=item_id)


async def on_roof_material_type_changed(event: ChatEvent, widget: ManagedWidget[Select], manager: DialogManager,
                                        item_id):
    ctx = manager.current_context()
    ctx.dialog_data.update(roof_material_type=item_id)


async def on_primorsky_region_changed(event: ChatEvent, widget: ManagedCheckboxAdapter, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(is_primorsky_region=ctx.widget_data.get(constants.ProposalForm.PRIMORSKY_REGION))
    if not ctx.dialog_data.get("is_primorsky_region"):
        ctx.dialog_data.update(estimate_type="house_kit")


async def on_partition_type_changed(event: ChatEvent, widget: ManagedWidget[Select], manager: DialogManager, item_id):
    ctx = manager.current_context()
    match ctx.state:
        case states.ProposalStates.select_ground_floor_panels_type:
            ctx.dialog_data.update(ground_floor_panel_type=item_id)
        case states.ProposalStates.select_exterior_walls_panels_type:
            ctx.dialog_data.update(exterior_wall_panel_type=item_id)
        case states.ProposalStates.select_attic_floor_panels_type:
            ctx.dialog_data.update(attic_floor_panel_type=item_id)
        case states.ProposalStates.select_internal_partitions_type:
            ctx.dialog_data.update(internal_partition_panel_type=item_id)
        case states.ProposalStates.select_intermediate_floor_type:
            ctx.dialog_data.update(intermediate_floor_panel_type=item_id)


async def on_enter_area(message: Message, message_input: MessageInput,
                        manager: DialogManager):
    ctx = manager.current_context()
    try:
        parser = CalcParser()
        lexer = CalcLexer()
        dimensions = message.text.split("*")
        built_up_area = format_decimal(parser.parse(lexer.tokenize(message.text)), pre=0)
        if len(dimensions) == 2:
            ctx.dialog_data.update(building_length=dimensions[0])
            ctx.dialog_data.update(building_width=dimensions[1])
        ctx.dialog_data.update(built_up_area=built_up_area)
    except RuntimeError:
        message_text = (f"Ошибка ввода {message.text}, необходимо целое число или "
                        f"произведение двух чисел вида ДЛИНА * ШИРИНА\n")
        await message.answer(message_text)
        return
    await manager.switch_to(states.ProposalStates.building_parameters)


async def on_enter_address(message: Message, message_input: MessageInput,
                           manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(address=message.text)

    await manager.switch_to(states.ProposalStates.estimate_type)
