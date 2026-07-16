"""NTCIP 1201 (1201v0227.mib) simulated data — type/range/DEFVAL aware.

SIM-DATA: see docs/1201DEFAULT_DATA.md
"""
from __future__ import annotations

from pysnmp.proto import rfc1902

from value_factory import wrap_int_for_syntax

# devices.1 = ASC device node (moduleDeviceNode reference)
ASC_DEVICE_OID = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1)
# timebaseAscActionTable pattern action reference example
ASC_PATTERN_ACTION_OID = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 5, 2, 1, 1, 0)

# Per-object scalar defaults (name -> RFC1902 value or int/str/oid tuple)
# INTEGER ranges use MIB maximum unless DEFVAL or semantics dictate otherwise.
SCALAR_VALUES: dict[str, object] = {
    # globalConfiguration
    "globalSetIDParameter": 65535,  # INTEGER (0..65535) max
    "globalMaxModules": 255,  # INTEGER (1..255) max
    "controllerBaseStandards": b"NTCIP 1201:v02.27\r\nNTCIP 1202:v02.18\r\nNTCIP 1103:v01.25",
    # globalDBManagement
    "dbCreateTransaction": 1,  # DEFVAL normal(1)
    "dbVerifyStatus": 3,  # doneWithNoError(3) — max enum
    "dbVerifyError": b"",  # empty when no error
    # globalTimeManagement
    "globalTime": ("Counter", 0),  # Counter DEFVAL {0}
    "globalDaylightSaving": 2,  # DEFVAL disableDST(2)
    "maxTimeBaseScheduleEntries": 65535,
    "timeBaseScheduleTable-status": 1,
    "maxDayPlans": 255,
    "maxDayPlanEvents": 255,
    "dayPlanStatus": 1,
    "controllerStandardTimeZone": 43200,  # INTEGER (-43200..43200) max
    "controllerLocalTime": ("Counter", 0),
    # profilesPMPP
    "maxGroupAddresses": 255,  # INTEGER (1..255) max
    # auxIO
    "auxIOTableNumDigitalPorts": 255,
    "auxIOTableNumAnalogPorts": 255,
}

# Column SYNTAX hints for large INTEGER / Counter columns in table templates
_COLUMN_SYNTAX: dict[str, str] = {
    "globalTime": "Counter",
    "controllerLocalTime": "Counter",
    "timeBaseScheduleDate": "INTEGER (0..4294967295)",
    "auxIOPortValue": "INTEGER (0..4294967295)",
    "auxIOPortLastCommandedState": "INTEGER (0..4294967295)",
}


def module_row_values(row: int) -> dict[str, object]:
    """globalModuleTable row template."""
    return {
        "moduleNumber": row,
        "moduleDeviceNode": ASC_DEVICE_OID,
        "moduleMake": b"SIM",
        "moduleModel": b"NTCIP1201-AGENT",
        "moduleVersion": b"20260706 - v1.0.0",
        "moduleType": 3,  # software(3)
    }


def time_base_schedule_row(row: int) -> dict[str, object]:
    return {
        "timeBaseScheduleNumber": row,
        "timeBaseScheduleMonth": 65535,  # INTEGER (0..65535) max bitmask
        "timeBaseScheduleDay": 255,  # INTEGER (0..255) max
        "timeBaseScheduleDate": 4294967295,  # INTEGER (0..4294967295) max
        "timeBaseScheduleDayPlan": min(row, 255),  # INTEGER (0..255)
    }


def day_plan_row(plan: int, event: int) -> dict[str, object]:
    return {
        "dayPlanNumber": plan,
        "dayPlanEventNumber": event,
        "dayPlanHour": 23,  # INTEGER (0..23) max
        "dayPlanMinute": 59,  # INTEGER (0..59) max
        "dayPlanActionNumberOID": ASC_PATTERN_ACTION_OID,
    }


def hdlc_group_address_row(row: int) -> dict[str, object]:
    return {
        "hdlcGroupAddressIndex": row,
        "hdlcGroupAddressNumber": 0,  # DEFVAL { 0 } — row disabled
    }


def aux_io_row(port_type: int, port_num: int) -> dict[str, object]:
    type_label = {2: b"Analog", 3: b"Digital"}.get(port_type, b"Other")
    direction = 2 if port_type == 3 else 1  # digital=input(2), analog=output(1)
    return {
        "auxIOPortType": port_type,
        "auxIOPortNumber": port_num,
        "auxIOPortDescription": type_label + b" Port " + str(port_num).encode(),
        "auxIOPortResolution": 32,  # INTEGER (1..32) max
        "auxIOPortValue": 4294967295,  # INTEGER (0..4294967295) max
        "auxIOPortDirection": direction,
        "auxIOPortLastCommandedState": 0,  # input ports = 0 per MIB
    }


TABLE_ROW_BUILDERS: dict[str, callable] = {
    "globalModuleTable": lambda i, j=0: module_row_values(i),
    "timeBaseScheduleTable": lambda i, j=0: time_base_schedule_row(i),
    "timeBaseDayPlanTable": lambda i, j: day_plan_row(i, j),
    "hdlcGroupAddressTable": lambda i, j=0: hdlc_group_address_row(i),
    "auxIOTable": lambda i, j: aux_io_row(i, j),
}


def value_for_1201_scalar(name: str):
    spec = SCALAR_VALUES.get(name)
    if spec is None:
        return None
    return _to_rfc1902(spec, name)


def value_for_1201_column(table_name: str, col_name: str, indices: tuple[int, ...]):
    builder = TABLE_ROW_BUILDERS.get(table_name)
    if not builder:
        return None
    if len(indices) == 1:
        row = builder(indices[0])
    elif len(indices) == 2:
        row = builder(indices[0], indices[1])
    else:
        return None
    spec = row.get(col_name)
    if spec is None:
        return None
    return _to_rfc1902(spec, col_name)


def _to_rfc1902(spec: object, name: str | None = None):
    if isinstance(spec, (rfc1902.Integer32, rfc1902.Counter32, rfc1902.Gauge32)):
        return spec
    if isinstance(spec, (rfc1902.OctetString, rfc1902.ObjectIdentifier)):
        return spec
    if isinstance(spec, tuple) and len(spec) == 2 and spec[0] == "Counter":
        return rfc1902.Counter32(int(spec[1]))
    if isinstance(spec, tuple):
        return rfc1902.ObjectIdentifier(spec)
    if isinstance(spec, bytes):
        return rfc1902.OctetString(spec)
    if isinstance(spec, int):
        syntax = _COLUMN_SYNTAX.get(name or "", "INTEGER")
        return wrap_int_for_syntax(spec, syntax)
    raise TypeError(spec)
