"""OID prefix helpers for NTCIP devices subtree."""
from __future__ import annotations

# transportation.devices — NTCIP 8004 { devices 2 }
DEVICES_OID_ROOT: tuple[int, ...] = (1, 3, 6, 1, 4, 1, 1206, 4, 2)

# devices.1 = asc (1202), devices.6 = global (1201 + 1103 report/security)
ASC_OID_ROOT: tuple[int, ...] = DEVICES_OID_ROOT + (1,)
GLOBAL_OID_ROOT: tuple[int, ...] = DEVICES_OID_ROOT + (6,)


def parse_oid_root(text: str | None) -> tuple[int, ...] | None:
    if not text:
        return None
    return tuple(int(x) for x in text.strip().split("."))


def oid_dotted(oid: tuple[int, ...]) -> str:
    return ".".join(str(x) for x in oid)


def under_prefix(oid: tuple[int, ...], prefix: tuple[int, ...] | None) -> bool:
    if prefix is None:
        return True
    return oid[: len(prefix)] == prefix
