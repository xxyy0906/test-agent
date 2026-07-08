"""Expand MIB tables to OID instances with simulated values."""
from __future__ import annotations

from sim_data.resolver import resolve_value
from smi_parser import ColumnDef, TableDef, index_limit_from_syntax

TABLE_INDEX_MAX: dict[str, list[str]] = {
    "globalModuleTable": ["globalMaxModules"],
    "timeBaseScheduleTable": ["maxTimeBaseScheduleEntries"],
    "timeBaseDayPlanTable": ["maxDayPlans", "maxDayPlanEvents"],
    "hdlcGroupAddressTable": ["maxGroupAddresses"],
    "eventClassTable": ["maxEventClasses"],
    "eventLogConfigTable": ["maxEventLogConfigs"],
    "eventLogTable": ["maxEventClasses", "eventLogNumber"],
    "communityNameTable": ["communityNamesMax"],
    "auxIOTable": [],  # expanded in expand_table (type × port)
    "phaseTable": ["maxPhases"],
    "phaseStatusGroupTable": ["maxPhaseGroups"],
    "phaseControlGroupTable": ["maxPhaseGroups"],
    "vehicleDetectorTable": ["maxVehicleDetectors"],
    "vehicleDetectorStatusGroupTable": ["maxVehicleDetectorStatusGroups"],
    "volumeOccupancyTable": ["maxVehicleDetectors"],
    "pedestrianDetectorTable": ["maxPedestrianDetectors"],
    "alarmGroupTable": ["maxAlarmGroups"],
    "specialFunctionOutputTable": ["maxSpecialFunctionOutputs"],
    "patternTable": ["maxPatterns"],
    "splitTable": ["maxSplits", "maxPhases"],
    "timebaseAscActionTable": ["maxTimebaseAscActions"],
    "preemptTable": ["maxPreempts"],
    "preemptControlTable": ["maxPreempts"],
    "sequenceTable": ["maxSequences", "maxRings"],
    "ringControlGroupTable": ["maxRingControlGroups"],
    "ringStatusTable": ["maxRings"],
    "channelTable": ["maxChannels"],
    "channelStatusGroupTable": ["maxChannelStatusGroups"],
    "overlapTable": ["maxOverlaps"],
    "overlapStatusGroupTable": ["maxOverlapStatusGroups"],
    "port1Table": ["maxPort1Addresses"],
    "dynObjDef": ["dynObjNumber", "dynObjIndex"],
    "logicalNameTranslationTable": ["logicalNameTranslation-index"],
}

TABLE_FALLBACK_ROWS: dict[str, int] = {
    "dynObjDef": 13,
    "logicalNameTranslationTable": 255,
    "characterTable": 255,
    "fontTable": 255,
}


def _scalar_limit(name: str, scalar_values: dict[str, int], syntax_by_name: dict[str, str]) -> int:
    if name in scalar_values:
        return max(1, scalar_values[name])
    if name in syntax_by_name:
        mx = index_limit_from_syntax(syntax_by_name[name])
        return max(1, mx)
    return 255


def _table_limits(
    table: TableDef,
    scalar_values: dict[str, int],
    syntax_by_name: dict[str, str],
    dev_cap: int | None,
) -> list[int]:
    if table.name in TABLE_INDEX_MAX:
        limits = []
        for idx_name in TABLE_INDEX_MAX[table.name]:
            if idx_name == "eventLogNumber":
                col = next((c for c in table.columns if c.name == "eventLogNumber"), None)
                lim = index_limit_from_syntax(col.syntax if col else "INTEGER (1..255)")
            elif idx_name == "dynObjIndex":
                lim = 255
            else:
                lim = _scalar_limit(idx_name, scalar_values, syntax_by_name)
            limits.append(max(1, lim))
        if dev_cap:
            limits = [min(x, dev_cap) for x in limits]
        return limits

    if table.name in TABLE_FALLBACK_ROWS:
        lim = TABLE_FALLBACK_ROWS[table.name]
        n = min(lim, dev_cap) if dev_cap else lim
        return [max(1, n)]

    if len(table.index_names) == 1:
        idx = table.index_names[0]
        col = next((c for c in table.columns if c.name == idx), None)
        lim = index_limit_from_syntax(col.syntax if col else "INTEGER (1..255)")
        if dev_cap:
            lim = min(lim, dev_cap)
        return [max(1, lim)]

    if len(table.index_names) == 2:
        limits = []
        for idx in table.index_names:
            col = next((c for c in table.columns if c.name == idx), None)
            lim = index_limit_from_syntax(col.syntax if col else "INTEGER (1..255)")
            if dev_cap:
                lim = min(lim, dev_cap)
            limits.append(max(1, lim))
        return limits

    lim = min(255, dev_cap) if dev_cap else 255
    return [max(1, lim)]


def _cell_value(
    table: TableDef,
    col: ColumnDef,
    indices: tuple[int, ...],
    index_value: int | None,
    syntax_by_name: dict[str, str],
):
    syn = syntax_by_name.get(col.name, col.syntax)
    return resolve_value(
        col.name,
        syn,
        defval=col.defval or None,
        index_value=index_value,
        is_index=col.is_index,
        table_name=table.name,
        indices=indices,
    )


def _expand_aux_io_table(
    table: TableDef,
    scalar_values: dict[str, int],
    syntax_by_name: dict[str, str],
    values: dict[tuple[int, ...], object],
    dev_cap: int | None,
) -> int:
    """auxIOTable INDEX { auxIOPortType, auxIOPortNumber } — analog(2) and digital(3) rows."""
    accessible = [c for c in table.columns if c.access != "not-accessible"]
    if not accessible:
        return 0

    analog_lim = _scalar_limit("auxIOTableNumAnalogPorts", scalar_values, syntax_by_name)
    digital_lim = _scalar_limit("auxIOTableNumDigitalPorts", scalar_values, syntax_by_name)
    if dev_cap:
        analog_lim = min(analog_lim, dev_cap)
        digital_lim = min(digital_lim, dev_cap)

    count = 0
    for port_type, lim in ((2, analog_lim), (3, digital_lim)):
        for port_num in range(1, lim + 1):
            indices = (port_type, port_num)
            for col in accessible:
                inst = table.base_oid + col.oid_suffix + indices
                if col.name == "auxIOPortType":
                    iv = port_type
                elif col.name == "auxIOPortNumber":
                    iv = port_num
                else:
                    iv = None
                values[inst] = _cell_value(table, col, indices, iv, syntax_by_name)
                count += 1
    return count


def expand_table(
    table: TableDef,
    scalar_values: dict[str, int],
    syntax_by_name: dict[str, str],
    values: dict[tuple[int, ...], object],
    dev_cap: int | None = None,
) -> int:
    if table.name == "auxIOTable":
        return _expand_aux_io_table(table, scalar_values, syntax_by_name, values, dev_cap)

    accessible = [c for c in table.columns if c.access != "not-accessible"]
    if not accessible:
        return 0

    limits = _table_limits(table, scalar_values, syntax_by_name, dev_cap)
    count = 0

    if len(limits) == 1:
        for i in range(1, limits[0] + 1):
            indices = (i,)
            for col in accessible:
                inst = table.base_oid + col.oid_suffix + indices
                iv = i if col.is_index else None
                values[inst] = _cell_value(table, col, indices, iv, syntax_by_name)
                count += 1
        return count

    if len(limits) == 2:
        for i in range(1, limits[0] + 1):
            for j in range(1, limits[1] + 1):
                indices = (i, j)
                for col in accessible:
                    inst = table.base_oid + col.oid_suffix + indices
                    if col.name == table.index_names[0]:
                        iv = i
                    elif len(table.index_names) > 1 and col.name == table.index_names[1]:
                        iv = j
                    elif col.is_index:
                        iv = i if col.name == table.index_names[0] else j
                    else:
                        iv = None
                    values[inst] = _cell_value(table, col, indices, iv, syntax_by_name)
                    count += 1
        return count

    for i in range(1, limits[0] + 1):
        indices = (i,)
        for col in accessible:
            inst = table.base_oid + col.oid_suffix + indices
            iv = i if col.is_index else None
            values[inst] = _cell_value(table, col, indices, iv, syntax_by_name)
            count += 1
    return count
