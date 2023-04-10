from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from tgbot.config import Settings
from . import constants, states
from ...models.db_commands import get_foundations, get_foundation, get_panel_partitions, get_internal_partitions, \
    intermediate_floor_partitions, get_partition, get_roofs, get_roof, get_roof_materials, get_roof_material, \
    get_estimate_types, get_estimate_type


async def proposal_form(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('db_session')
    config: Settings = middleware_data.get("config")
    ctx = dialog_manager.current_context()
    start_data = ctx.start_data
    dialog_data = ctx.dialog_data

    started_by = start_data.get("started_by") or "UNKNOWN"
    built_up_area = ctx.dialog_data.get("built_up_area") or 0
    building_length = ctx.dialog_data.get("building_length") or 0
    building_width = ctx.dialog_data.get("building_width") or 0
    dimensions = f"({building_length} м * {building_width} м)" if building_length and building_width else ""
    building_params_state = "✅ " if built_up_area else ""
    building_params = f"{built_up_area} м2 {dimensions}"

    number_floors_state = "✅ " if (num_f := ctx.dialog_data.get("number_floors")) else ""
    number_floors = num_f or ""

    foundation_type_state = "✅ " if (_t := ctx.dialog_data.get("foundation_type")) else ""
    foundation = get_foundation(_t)
    foundation_name = foundation.name if foundation else ""

    ground_floor_panel_state = "✅ " if (_t := ctx.dialog_data.get("ground_floor_panel_type")) else ""
    ground_floor_panel = get_partition(_t)
    ground_floor_panel_name = ground_floor_panel.name if ground_floor_panel else ""

    intermediate_floor_panel_state = "✅ " if (_t := ctx.dialog_data.get("intermediate_floor_panel_type")
                                              ) or (len(number_floors) and int(number_floors) < 2) else ""
    intermediate_floor_panel = get_partition(_t)
    intermediate_floor_panel_name = intermediate_floor_panel.name if intermediate_floor_panel else ""

    attic_floor_panel_state = "✅ " if (_t := ctx.dialog_data.get("attic_floor_panel_type")) else ""
    attic_floor_panel = get_partition(_t)
    attic_floor_panel_name = attic_floor_panel.name if attic_floor_panel else ""

    exterior_wall_panel_state = "✅ " if (_t := ctx.dialog_data.get("exterior_wall_panel_type")) else ""
    exterior_wall_panel = get_partition(_t)
    exterior_wall_panel_name = exterior_wall_panel.name if exterior_wall_panel else ""

    internal_partition_panel_state = "✅ " if (_t := ctx.dialog_data.get("internal_partition_panel_type")) else ""
    internal_partition_panel = get_partition(_t)
    internal_partition_panel_name = internal_partition_panel.name if internal_partition_panel else ""

    roof_state = "✅ " if (_t := ctx.dialog_data.get("roof_type")) else ""
    roof = get_roof(_t)
    roof_name = roof.name if roof else ""

    roof_material_state = "✅ " if (_t := ctx.dialog_data.get("roof_material_type")) else ""
    roof_material = get_roof_material(_t)
    roof_material_name = roof_material.name if roof_material else ""

    address_state = "✅ " if (_t := ctx.dialog_data.get("address")) else ""
    address = _t or ""

    estimate_state = "✅ " if (_t := ctx.dialog_data.get("estimate_type")) else ""
    estimate = get_estimate_type(_t)
    estimate_name = estimate.name if estimate else ""

    return {"started_by": started_by,
            "building_params_state": building_params_state,
            "building_params": building_params,
            "number_floors_state": number_floors_state,
            "number_floors": number_floors,
            "foundation_type_state": foundation_type_state,
            "foundation_name": foundation_name,
            "ground_floor_panel_state": ground_floor_panel_state,
            "ground_floor_panel_name": ground_floor_panel_name,
            "intermediate_floor_panel_state": intermediate_floor_panel_state,
            "intermediate_floor_panel_name": intermediate_floor_panel_name,
            "attic_floor_panel_state": attic_floor_panel_state,
            "attic_floor_panel_name": attic_floor_panel_name,
            "exterior_wall_panel_state": exterior_wall_panel_state,
            "exterior_wall_panel_name": exterior_wall_panel_name,
            "internal_partition_panel_state": internal_partition_panel_state,
            "internal_partition_panel_name": internal_partition_panel_name,
            "roof_state": roof_state,
            "roof_name": roof_name,
            "roof_material_state": roof_material_state,
            "roof_material_name": roof_material_name,
            "address_state": address_state,
            "address": address,
            "estimate_state": estimate_state,
            "estimate_name": estimate_name}


async def building_parameters(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('db_session')
    config: Settings = middleware_data.get("config")
    ctx = dialog_manager.current_context()
    dialog_data = ctx.dialog_data

    number_floors_list = [(f"{i} этаж{'a' if i > 1 else ''}", i) for i in range(1, 4)]

    built_up_area = ctx.dialog_data.get("built_up_area") or 0
    building_length = ctx.dialog_data.get("building_length") or 0
    building_width = ctx.dialog_data.get("building_width") or 0
    dimensions = f"({building_length} м * {building_width} м)" if building_length and building_width else ""
    building_params = f"{built_up_area} м2 {dimensions}"
    number_floors = ctx.dialog_data.get("number_floors") or ""

    return {"number_floors_list": number_floors_list,
            "building_params": building_params,
            "number_floors": number_floors}


async def foundation_form(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('db_session')
    config: Settings = middleware_data.get("config")
    ctx = dialog_manager.current_context()
    dialog_data = ctx.dialog_data

    foundations = get_foundations()
    foundation_type = dialog_data.get("foundation_type") or ""
    foundation = get_foundation(foundation_type)
    description = foundation.description if foundation else ""
    if foundation:
        image = MediaAttachment(type=ContentType.PHOTO, path=foundation.media)
    else:
        foundation = get_foundation("type-1")
        image = MediaAttachment(type=ContentType.PHOTO, path=foundation.media)

    select_types_kbd = dialog_manager.find(constants.ProposalForm.SELECT_FOUNDATION_TYPE)
    await select_types_kbd.set_checked(item_id=foundation_type)
    return {"foundations": foundations,
            "image": image,
            "description": description}


async def roof_form(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('db_session')
    config: Settings = middleware_data.get("config")
    ctx = dialog_manager.current_context()
    dialog_data = ctx.dialog_data

    roofs = get_roofs()
    roof_type = dialog_data.get("roof_type") or ""
    roof = get_roof(roof_type)
    description = roof.description if roof else ""
    if roof:
        image = MediaAttachment(type=ContentType.PHOTO, path=roof.media)
    else:
        roof = get_roof("slope-1")
        image = MediaAttachment(type=ContentType.PHOTO, path=roof.media)

    select_types_kbd = dialog_manager.find(constants.ProposalForm.SELECT_ROOF_TYPE)
    await select_types_kbd.set_checked(item_id=roof_type)
    return {"roofs": roofs,
            "image": image,
            "description": description}


async def roof_material_form(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('db_session')
    config: Settings = middleware_data.get("config")
    ctx = dialog_manager.current_context()
    dialog_data = ctx.dialog_data

    roof_materials = get_roof_materials()
    roof_material_type = dialog_data.get("roof_material_type") or ""
    roof_material = get_roof_material(roof_material_type)
    description = roof_material.description if roof_material else ""
    if roof_material:
        image = MediaAttachment(type=ContentType.PHOTO, path=roof_material.media)
    else:
        roof_material = get_roof_material("type-1")
        image = MediaAttachment(type=ContentType.PHOTO, path=roof_material.media)

    select_types_kbd = dialog_manager.find(constants.ProposalForm.SELECT_ROOFING_MATERIAL)
    await select_types_kbd.set_checked(item_id=roof_material_type)
    return {"roof_materials": roof_materials,
            "image": image,
            "description": description}


async def partition_form(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('db_session')
    config: Settings = middleware_data.get("config")
    ctx = dialog_manager.current_context()
    dialog_data = ctx.dialog_data

    partitions = get_panel_partitions()
    match ctx.state:
        case states.ProposalStates.select_ground_floor_panels_type:
            partition_type = dialog_data.get("ground_floor_panel_type") or "sip-1_None"
        case states.ProposalStates.select_exterior_walls_panels_type:
            partition_type = dialog_data.get("exterior_wall_panel_type") or "sip-1_None"
        case states.ProposalStates.select_attic_floor_panels_type:
            partitions = get_internal_partitions()
            partition_type = dialog_data.get("attic_floor_panel_type") or "frame-1_None"
        case states.ProposalStates.select_internal_partitions_type:
            partitions = get_internal_partitions()
            partition_type = dialog_data.get("internal_partition_panel_type") or "frame-1_None"
        case states.ProposalStates.select_intermediate_floor_type:
            partitions = intermediate_floor_partitions()
            partition_type = dialog_data.get("intermediate_floor_panel_type") or "frame-1_None"
        case _:
            partition_type = "sip-1_None"

    partition = get_partition(partition_type)
    description = partition.description if partition else ""
    if partition:
        image = MediaAttachment(type=ContentType.PHOTO, path=partition.media)
    else:
        if partition_type.endswith("None"):
            partition = get_partition(partition_type[0:-5])
        image = MediaAttachment(type=ContentType.PHOTO, path=partition.media)

    select_types_kbd = dialog_manager.find(constants.ProposalForm.CONSTRUCTION_TYPES)
    await select_types_kbd.set_checked(item_id=partition_type)

    return {"partitions": partitions,
            "image": image,
            "description": description}


async def address_estimate(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('db_session')
    config: Settings = middleware_data.get("config")
    ctx = dialog_manager.current_context()
    estimate_types = get_estimate_types()

    dialog_data = ctx.dialog_data
    address = dialog_data.get("address") or ""

    estimate_type = dialog_data.get("estimate_type") or ""
    estimate = get_estimate_type(estimate_type)
    estimate_name = estimate.name if estimate else ""
    estimate_types_kbd = dialog_manager.find(constants.ProposalForm.SELECT_ESTIMATE_TYPE)
    await estimate_types_kbd.set_checked(item_id=estimate_type)
    return {"address": address,
            "estimate_name": estimate_name,
            "estimate_types": estimate_types}
