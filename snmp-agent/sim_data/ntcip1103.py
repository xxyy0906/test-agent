"""NTCIP 1103 simulated data for objects under global (devices.6)."""
from __future__ import annotations

from pysnmp.proto import rfc1902

from value_factory import wrap_int_for_syntax


def community_name_row(row: int) -> dict[str, object]:
    """communityNameTable — DEFVAL public + full write mask."""
    names = {1: b"public", 2: b"administrator"}
    return {
        "communityNameIndex": row,
        "communityNameUser": names.get(row, b"public"),
        "communityNameAccessMask": 4294967295,  # Gauge DEFVAL { 4294967295 }
    }


TABLE_ROW_BUILDERS: dict[str, callable] = {
    "communityNameTable": lambda i, j=0: community_name_row(i),
}


def value_for_1103_column(table_name: str, col_name: str, indices: tuple[int, ...]):
    builder = TABLE_ROW_BUILDERS.get(table_name)
    if not builder or len(indices) != 1:
        return None
    spec = builder(indices[0]).get(col_name)
    if spec is None:
        return None
    if col_name == "communityNameAccessMask":
        return wrap_int_for_syntax(int(spec), "Gauge")
    if isinstance(spec, bytes):
        return rfc1902.OctetString(spec)
    if isinstance(spec, int):
        return rfc1902.Integer32(spec)
    raise TypeError(spec)
