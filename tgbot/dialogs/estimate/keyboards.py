import operator

from aiogram_dialog.widgets.kbd import Row, Radio, Group, Button, SwitchTo, Select, Checkbox
from aiogram_dialog.widgets.text import Format, Const

from . import constants, events, states, whenable

MAIN_MENU_BUTTON = SwitchTo(
    text=Const("☰ Главное меню"),
    id="__main__",
    state=states.ProposalStates.start_window,
)


def main_menu_kbd():
    return Group(
        SwitchTo(Const("Размер и этажность"),
                 id=constants.ProposalForm.BUILDING_PARAMETERS_BUTTON,
                 state=states.ProposalStates.building_parameters),
        SwitchTo(Const("Тип фундамента"),
                 id=constants.ProposalForm.SELECT_FOUNDATION_BUTTON,
                 state=states.ProposalStates.select_foundation_type),
        SwitchTo(Const("Нулевое перекрытие"),
                 id=constants.ProposalForm.SELECT_GROUND_FLOOR_PANELS_TYPE,
                 state=states.ProposalStates.select_ground_floor_panels_type),
        SwitchTo(Const("Межэтажное перекрытие"),
                 id=constants.ProposalForm.SELECT_INTERMEDIATE_FLOOR_TYPE,
                 state=states.ProposalStates.select_intermediate_floor_type,
                 when=whenable.is_multi_floor),
        SwitchTo(Const("Чердачное перекрытие"),
                 id=constants.ProposalForm.SELECT_ATTIC_FLOOR_PANELS_TYPE,
                 state=states.ProposalStates.select_attic_floor_panels_type),
        SwitchTo(Const("Наружные стены"),
                 state=states.ProposalStates.select_exterior_walls_panels_type,
                 id=constants.ProposalForm.SELECT_EXTERIOR_WALLS_PANELS_TYPE),
        SwitchTo(Const("Внутренние перегородки"),
                 id=constants.ProposalForm.SELECT_INTERNAL_PARTITIONS_TYPE,
                 state=states.ProposalStates.select_internal_partitions_type),
        SwitchTo(Const("Крыша"),
                 id=constants.ProposalForm.SELECT_ROOF_BUTTON,
                 state=states.ProposalStates.select_roof_type),
        SwitchTo(Const("Кровля"),
                 id=constants.ProposalForm.SELECT_ROOFING_MATERIAL_BUTTON,
                 state=states.ProposalStates.select_roof_material),
        SwitchTo(Const("Адрес и вид расчета"),
                 id=constants.ProposalForm.ENTER_BUILDING_ADDRESS,
                 state=states.ProposalStates.estimate_type),

        width=2

    )


def building_parameters_kbd():
    return Group(
        Row(
            Radio(
                Format("✅ {item[0]}"),
                Format("  {item[0]}"),
                id=constants.ProposalForm.SELECT_NUMBER_FLOORS,
                item_id_getter=operator.itemgetter(1),
                on_state_changed=events.on_number_floors_changed,
                items="number_floors_list"
            )
        ),
        SwitchTo(Const("✍️ Площадь застройки"),
                 id=constants.ProposalForm.ENTER_BUILT_UP_AREA,
                 state=states.ProposalStates.enter_built_up_area_area),
        MAIN_MENU_BUTTON
    )


def select_types_kbd(widget_id, on_state_changed, items):
    return Group(
        Radio(
            Format("✅ {item.name}"),
            Format("  {item.name}"),
            id=widget_id,
            item_id_getter=operator.attrgetter("type"),
            on_state_changed=on_state_changed,
            items=items
        ),
        MAIN_MENU_BUTTON,
        width=1
    )


def select_address_kbd():
    return Group(
        Row(
            Checkbox(Const("✅ Приморский край"),
                     Const("Приморский край"),
                     id=constants.ProposalForm.PRIMORSKY_REGION,
                     on_state_changed=events.on_primorsky_region_changed,
                     default=True),
            SwitchTo(Const("✍️ Укажите адрес"),
                     id=constants.ProposalForm.ENTER_BUILDING_ADDRESS,
                     state=states.ProposalStates.enter_building_address)
        ),
        Row(
            Radio(
                Format("✅ {item.name}"),
                Format("  {item.name}"),
                id=constants.ProposalForm.SELECT_ESTIMATE_TYPE,
                item_id_getter=operator.attrgetter("code"),
                on_state_changed=events.on_estimate_type_changed,
                items="estimate_types"
            ),
            when=whenable.is_primorsky_region
        ),
        MAIN_MENU_BUTTON
    )
