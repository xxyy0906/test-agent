"""NTCIP 1202 (1202v0218.mib) simulated data — type/range/DEFVAL aware.

SIM-DATA: see docs/1202DEFAULT_DATA.md and tree/1202v0218-tree.md
"""
from __future__ import annotations

from pysnmp.proto import rfc1902

from value_factory import wrap_int_for_syntax

ASC_ROOT_OID = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1)
TIMEBASE_ASC_ACTION_OID = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 5, 2, 1, 1, 0)

# Scalars where semantic value differs from generic range-max
SCALAR_VALUES: dict[str, object] = {}

# Large INTEGER / Counter column hints
_COLUMN_SYNTAX: dict[str, str] = {
    "preemptDelay": "INTEGER (0..65535)",
    "preemptMinimumDuration": "INTEGER (0..65535)",
    "preemptDwellGreen": "INTEGER (0..65535)",
}


def _phase_row(row: int) -> dict[str, object]:
    return {"phaseNumber": row}


def _vehicle_detector_row(row: int) -> dict[str, object]:
    return {"vehicleDetectorNumber": row}


def _pedestrian_detector_row(row: int) -> dict[str, object]:
    return {"pedestrianDetectorNumber": row}


def _preempt_row(row: int) -> dict[str, object]:
    """Only INDEX column; other columns use MIB DEFVAL via resolver."""
    return {"preemptNumber": row}


def _port1_row(row: int) -> dict[str, object]:
    return {
        "port1AddressIndex": row,
        "port1Address": b"",
        "port1DeviceType": b"",
        "port1Description": b"",
    }


def _asc_block_row(row: int) -> dict[str, object]:
    return {
        "ascBlockGetControl": 0,
        "ascBlockData": b"",
    }


TABLE_ROW_BUILDERS: dict[str, callable] = {
    "phaseTable": lambda i, j=0: _phase_row(i),
    "vehicleDetectorTable": lambda i, j=0: _vehicle_detector_row(i),
    "pedestrianDetectorTable": lambda i, j=0: _pedestrian_detector_row(i),
    "preemptTable": lambda i, j=0: _preempt_row(i),
    "port1Table": lambda i, j=0: _port1_row(i),
}


def value_for_1202_scalar(name: str):
    spec = SCALAR_VALUES.get(name)
    if spec is None:
        return None
    return _to_rfc1902(spec, name)


def value_for_1202_column(table_name: str, col_name: str, indices: tuple[int, ...]):
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
    if isinstance(spec, rfc1902.Integer32 | rfc1902.Counter32 | rfc1902.Gauge32):
        return spec
    if isinstance(spec, rfc1902.OctetString | rfc1902.ObjectIdentifier):
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
