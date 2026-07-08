"""Generate SNMP values at MIB syntax maximums."""
from __future__ import annotations

import re
from pysnmp.proto import rfc1902

_ENUM_ITEM = re.compile(r"\(\s*(\d+)\s*\)")
_RANGE = re.compile(r"\(\s*(-?\d+)\s*\.\.\s*(-?\d+)\s*\)")
_SIZE = re.compile(r"SIZE\s*\(\s*(\d+)\s*\.\.\s*(\d+)\s*\)", re.I)

# SIM-DATA: see docs/DEFAULT_DATA.md and docs/1202DEFAULT_DATA.md
NTCIP_DEFAULT_OID = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 6, 255)


def _max_enum(syntax: str) -> int:
    nums = [int(m.group(1)) for m in _ENUM_ITEM.finditer(syntax)]
    return max(nums) if nums else 1


def _max_range(syntax: str) -> int | None:
    m = _RANGE.search(syntax)
    if not m:
        return None
    lo, hi = int(m.group(1)), int(m.group(2))
    if lo < 0 and hi > 0:
        return hi if abs(hi) >= abs(lo) else lo
    return hi


def _octet_max(syntax: str) -> int:
    m = _SIZE.search(syntax)
    if m:
        return int(m.group(2))
    if "DisplayString" in syntax or "OwnerString" in syntax or "OerString" in syntax:
        return 255
    return 255


def wrap_int_for_syntax(value: int, syntax: str):
    """Map a numeric value to the correct RFC1902 type for the MIB SYNTAX."""
    syntax_u = syntax.strip()
    syntax_l = syntax_u.lower()

    if syntax_l.startswith("counter") or syntax_u.startswith("Counter"):
        return rfc1902.Counter32(value & 0xFFFFFFFF)

    if syntax_l.startswith("gauge") or syntax_u.startswith("Gauge"):
        return rfc1902.Gauge32(value & 0xFFFFFFFF)

    if syntax_l.startswith("integer") or syntax_u.startswith("INTEGER"):
        rng = _max_range(syntax_u)
        if rng is not None and rng > 2147483647:
            return rfc1902.Gauge32(value)
        return rfc1902.Integer32(value)

    if "{" in syntax_u:
        return rfc1902.Integer32(value)

    if value > 2147483647:
        return rfc1902.Gauge32(value)
    return rfc1902.Integer32(value)


def max_value_for_syntax(syntax: str, index_value: int | None = None):
    """Return a pysnmp RFC1902 value at the syntax maximum."""
    syntax_u = syntax.strip()
    syntax_l = syntax_u.lower()

    if index_value is not None and ("integer" in syntax_l or syntax_u.startswith("INTEGER")):
        if "enum" not in syntax_l and "{" not in syntax_u:
            rng = _RANGE.search(syntax_u)
            if rng:
                lo, hi = int(rng.group(1)), int(rng.group(2))
                return rfc1902.Integer32(min(max(index_value, lo), hi))
            return rfc1902.Integer32(index_value)

    if syntax_u.startswith("Enum") or ("{" in syntax_u and "integer" not in syntax_l):
        return rfc1902.Integer32(_max_enum(syntax_u))

    if syntax_l.startswith("integer") or syntax_u.startswith("INTEGER"):
        rng = _max_range(syntax_u)
        if rng is None:
            return rfc1902.Integer32(2147483647)
        if rng > 2147483647:
            return rfc1902.Gauge32(rng)
        return rfc1902.Integer32(rng)

    if syntax_l.startswith("counter") or syntax_u.startswith("Counter"):
        return rfc1902.Counter32(4294967295)

    if syntax_l.startswith("gauge") or syntax_u.startswith("Gauge"):
        rng = _max_range(syntax_u)
        return rfc1902.Gauge32(rng if rng is not None else 4294967295)

    if syntax_l.startswith("timeticks"):
        return rfc1902.TimeTicks(4294967295)

    if syntax_l.startswith("objectid") or syntax_u.startswith("ObjectID") or syntax_u.startswith("OBJECT IDENTIFIER"):
        return rfc1902.ObjectIdentifier(NTCIP_DEFAULT_OID)

    if syntax_l.startswith("opaque") or syntax_u.startswith("Opaque"):
        n = _octet_max(syntax_u)
        return rfc1902.Opaque(bytes([0xFF] * min(n, 255)))

    if any(x in syntax_l for x in ("octet", "displaystring", "ownerstring", "oerstring", "bitmap")):
        n = _octet_max(syntax_u)
        if "bitmap" in syntax_l and not _SIZE.search(syntax_u):
            n = 1
        return rfc1902.OctetString(b"Z" * n)

    if syntax_l.startswith("physaddress"):
        return rfc1902.OctetString(bytes([0xFF] * 6))

    if syntax_l.startswith("networkaddress"):
        return rfc1902.IpAddress("255.255.255.255")

    if syntax_u in ("Byte", "Ubyte", "Short", "Ushort", "Long"):
        rng = _max_range(syntax_u.replace("Ubyte", "INTEGER (0..255)"))
        if rng is not None:
            return rfc1902.Integer32(rng)

    rng = _max_range(syntax_u)
    if rng is not None:
        return rfc1902.Integer32(rng)

    return rfc1902.Integer32(2147483647)
