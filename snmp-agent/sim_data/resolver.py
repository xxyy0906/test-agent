"""Resolve simulated SNMP values from MIB type, range, DEFVAL, and module rules."""
from __future__ import annotations

import re

from pysnmp.proto import rfc1902

from sim_data import ntcip1103, ntcip1201, ntcip1202
from value_factory import max_value_for_syntax, wrap_int_for_syntax

_ENUM_ITEM = re.compile(r"\(\s*(-?\d+)\s*\)")
_ENUM_NAME = re.compile(r"(\w+)\s*\(\s*(-?\d+)\s*\)")
_RANGE = re.compile(r"\(\s*(-?\d+)\s*\.\.\s*(-?\d+)\s*\)")
_SIZE = re.compile(r"SIZE\s*\(\s*(\d+)\s*\.\.\s*(\d+)\s*\)", re.I)

_DEFVAL_MAP = {
    "normal": 1,
    "transaction": 2,
    "verify": 3,
    "done": 6,
    "notdone": 1,
    "donewitherror": 2,
    "donewithnoerror": 3,
    "disabledst": 2,
    "null": None,
}


def _parse_defval(raw: str | None, syntax: str = "") -> int | str | bytes | None:
    if not raw:
        return None
    text = raw.strip()
    if text.startswith("{") and text.endswith("}"):
        text = text[1:-1].strip()
    token = text.lower().replace("-", "").replace("_", "")
    if token in _DEFVAL_MAP:
        return _DEFVAL_MAP[token]
    # enum DEFVAL: name(N) or name (N)
    em = _ENUM_NAME.search(text)
    if em and "{" in syntax:
        return int(em.group(2))
    if token.isdigit() or (token.startswith("-") and token[1:].isdigit()):
        return int(token)
    if text.startswith('"') or text.startswith("'"):
        return text.strip('"').strip("'").encode("ascii")
    return None


def _range_bounds(syntax: str) -> tuple[int, int] | None:
    m = _RANGE.search(syntax)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def _enum_values(syntax: str) -> list[int]:
    return [int(x.group(1)) for x in _ENUM_ITEM.finditer(syntax)]


def _is_enum_syntax(syntax: str) -> bool:
    syntax_l = syntax.lower()
    return bool(_ENUM_ITEM.search(syntax)) and (
        "integer" in syntax_l or syntax.strip().upper().startswith("INTEGER")
    )


def _octet_fill(syntax: str) -> bytes:
    m = _SIZE.search(syntax)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        if hi == 0:
            return b""
        if lo == 0:
            return b""
        return b"Z" * min(hi, 255)
    return b"Z" * 255


def resolve_value(
    name: str,
    syntax: str,
    *,
    defval: str | None = None,
    index_value: int | None = None,
    is_index: bool = False,
    table_name: str | None = None,
    indices: tuple[int, ...] | None = None,
):
    """Return RFC1902 value obeying MIB SYNTAX, DEFVAL, and module sim rules."""
    syntax_u = re.sub(r"\s+", " ", syntax.strip())
    syntax_l = syntax_u.lower()

    if table_name and indices is not None:
        v = ntcip1201.value_for_1201_column(table_name, name, indices)
        if v is not None:
            return v
        v = ntcip1202.value_for_1202_column(table_name, name, indices)
        if v is not None:
            return v
        v = ntcip1103.value_for_1103_column(table_name, name, indices)
        if v is not None:
            return v
    if table_name is None and not is_index:
        v = ntcip1201.value_for_1201_scalar(name)
        if v is not None:
            return v
        v = ntcip1202.value_for_1202_scalar(name)
        if v is not None:
            return v

    if is_index and index_value is not None:
        return max_value_for_syntax(syntax_u, index_value=index_value)

    parsed = _parse_defval(defval, syntax_u)
    if defval and "null" in defval.lower():
        return rfc1902.ObjectIdentifier((0, 0))
    if isinstance(parsed, int):
        return wrap_int_for_syntax(parsed, syntax_u)
    if isinstance(parsed, bytes):
        return rfc1902.OctetString(parsed)

    if syntax_l.startswith("counter"):
        return rfc1902.Counter32(4294967295)

    if syntax_l.startswith("gauge"):
        bounds = _range_bounds(syntax_u)
        return rfc1902.Gauge32(bounds[1] if bounds else 4294967295)

    if _is_enum_syntax(syntax_u):
        enums = _enum_values(syntax_u)
        return rfc1902.Integer32(max(enums) if enums else 1)

    if syntax_l.startswith("integer") or syntax_u.upper().startswith("INTEGER"):
        bounds = _range_bounds(syntax_u)
        if bounds:
            lo, hi = bounds
            if hi > 2147483647:
                return rfc1902.Gauge32(hi)
            return rfc1902.Integer32(hi)
        return rfc1902.Integer32(2147483647)

    if syntax_l.startswith("object identifier"):
        return rfc1902.ObjectIdentifier(ntcip1202.ASC_ROOT_OID)

    if any(x in syntax_l for x in ("octet", "displaystring", "ownerstring")):
        return rfc1902.OctetString(_octet_fill(syntax_u))

    if syntax_l.startswith("opaque"):
        return rfc1902.Opaque(b"\xff" * 255)

    return max_value_for_syntax(syntax_u, index_value=index_value)
