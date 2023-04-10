from aiogram.fsm.state import StatesGroup, State


class ProposalStates(StatesGroup):
    start_window = State()
    building_parameters = State()
    select_number_of_floors = State()
    enter_built_up_area_area = State()
    select_foundation_type = State()
    select_ground_floor_panels_type = State()
    select_exterior_walls_panels_type = State()
    select_attic_floor_panels_type = State()
    select_internal_partitions_type = State()
    select_intermediate_floor_type = State()
    select_roof_type = State()
    select_roof_material = State()
    estimate_type = State()
    enter_building_address = State()



