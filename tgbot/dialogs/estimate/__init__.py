from aiogram_dialog import Dialog

from . import windows, events, states, getters, constants


def estimate_dialogs():
    return [
        Dialog(
            windows.proposal_window(),
            windows.building_parameters_window(),
            windows.proposal_input_window(text=("Укажите площадь застройки "
                                                "в виде одного числа (например 200) "
                                                "или произведения длина*ширина (например 10*20)\n"
                                                "👇 Площадь застройки 👇"),
                                          handler=events.on_enter_area,
                                          state=states.ProposalStates.enter_built_up_area_area,
                                          getter=getters.proposal_form),
            windows.construction_types_window(state=states.ProposalStates.select_foundation_type,
                                              getter=getters.foundation_form,
                                              widget_id=constants.ProposalForm.SELECT_FOUNDATION_TYPE,
                                              on_state_changed=events.on_foundation_type_changed,
                                              items="foundations"),
            windows.construction_types_window(state=states.ProposalStates.select_ground_floor_panels_type,
                                              getter=getters.partition_form,
                                              widget_id=constants.ProposalForm.CONSTRUCTION_TYPES,
                                              on_state_changed=events.on_partition_type_changed,
                                              items="partitions"),
            windows.construction_types_window(state=states.ProposalStates.select_exterior_walls_panels_type,
                                              getter=getters.partition_form,
                                              widget_id=constants.ProposalForm.CONSTRUCTION_TYPES,
                                              on_state_changed=events.on_partition_type_changed,
                                              items="partitions"),
            windows.construction_types_window(state=states.ProposalStates.select_attic_floor_panels_type,
                                              getter=getters.partition_form,
                                              widget_id=constants.ProposalForm.CONSTRUCTION_TYPES,
                                              on_state_changed=events.on_partition_type_changed,
                                              items="partitions"),
            windows.construction_types_window(state=states.ProposalStates.select_internal_partitions_type,
                                              getter=getters.partition_form,
                                              widget_id=constants.ProposalForm.CONSTRUCTION_TYPES,
                                              on_state_changed=events.on_partition_type_changed,
                                              items="partitions"),
            windows.construction_types_window(state=states.ProposalStates.select_intermediate_floor_type,
                                              getter=getters.partition_form,
                                              widget_id=constants.ProposalForm.CONSTRUCTION_TYPES,
                                              on_state_changed=events.on_partition_type_changed,
                                              items="partitions"),
            windows.construction_types_window(state=states.ProposalStates.select_roof_type,
                                              getter=getters.roof_form,
                                              widget_id=constants.ProposalForm.SELECT_ROOF_TYPE,
                                              on_state_changed=events.on_roof_type_changed,
                                              items="roofs"),
            windows.construction_types_window(state=states.ProposalStates.select_roof_material,
                                              getter=getters.roof_material_form,
                                              widget_id=constants.ProposalForm.SELECT_ROOFING_MATERIAL,
                                              on_state_changed=events.on_roof_material_type_changed,
                                              items="roof_materials"),
            windows.address_window(),
            windows.proposal_input_window(text=("👇 Введите адрес объекта 👇"),
                                          handler=events.on_enter_address,
                                          state=states.ProposalStates.enter_building_address,
                                          getter=getters.proposal_form),
            on_start=None,
            on_process_result=None
        )
    ]
