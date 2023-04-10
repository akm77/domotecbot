from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const

from . import states, getters, keyboards

PROPOSAL_FORM = ("Расчет для: {started_by}\n"
                 "<pre>------------------------------</pre>\n"
                 "{building_params_state}Площадь застройки: <b>{building_params}</b>\n"
                 "{number_floors_state}Этажность: <b>{number_floors}</b> эт.\n"
                 "{foundation_type_state}Тип фундамента: <b>{foundation_name}</b>\n"
                 "{ground_floor_panel_state}Нулевое перекрытие: <b>{ground_floor_panel_name}</b>\n"
                 "{intermediate_floor_panel_state}Межэтажное перекрытие: <b>{intermediate_floor_panel_name}</b>\n"
                 "{attic_floor_panel_state}Чердачное перекрытие: <b>{attic_floor_panel_name}</b>\n"
                 "{exterior_wall_panel_state}Наружные стены: <b>{exterior_wall_panel_name}</b>\n"
                 "{internal_partition_panel_state}Внутренние перегородки: <b>{internal_partition_panel_name}</b>\n"
                 "{roof_state}Крыша: <b>{roof_name}</b>\n"
                 "{roof_material_state}Кровля: <b>{roof_material_name}</b>\n"
                 "{address_state}Адрес: <b>{address}</b>\n"
                 "{estimate_state}Вид расчета: <b>{estimate_name}</b>")

BUILDING_PARAMETERS_FORM = ("Укажимте размер дома\n"
                            "Этажность: <b>{number_floors}</b> эт.\n"
                            "Площадь застройки: <b>{building_params}</b>")

ADDRESS_FORM = ("Укажите адрес и вид расчета:\n"
                "Адрес: <b>{address}</b>\n"
                "Вид расчета: <b>{estimate_name}</b>")


def proposal_window():
    return Window(Format(PROPOSAL_FORM),
                  keyboards.main_menu_kbd(),
                  Cancel(Const("<<")),
                  state=states.ProposalStates.start_window,
                  getter=getters.proposal_form)


def proposal_input_window(text: str, handler=None, state=None, getter=None):
    return Window(
        Format(text),
        MessageInput(handler,
                     content_types=[ContentType.TEXT]),
        state=state,
        getter=getter
    )


def building_parameters_window():
    return Window(
        Format(BUILDING_PARAMETERS_FORM),
        keyboards.building_parameters_kbd(),
        state=states.ProposalStates.building_parameters,
        getter=getters.building_parameters
    )


def construction_types_window(state, getter, widget_id, on_state_changed, items):
    return Window(
        DynamicMedia(selector="image"),
        Format("{description}"),
        keyboards.select_types_kbd(widget_id=widget_id, on_state_changed=on_state_changed, items=items),
        state=state,
        getter=getter
    )


def address_window():
    return Window(
        Format(ADDRESS_FORM),
        keyboards.select_address_kbd(),
        state=states.ProposalStates.estimate_type,
        getter=getters.address_estimate
    )
