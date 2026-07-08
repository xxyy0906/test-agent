"""Validate simulated SNMP values against MIB SYNTAX ranges."""
from __future__ import annotations

import re

_ENUM = re.compile(r"\(\s*(-?\d+)\s*\)")
_RANGE = re.compile(r"\(\s*(-?\d+)\s*\.\.\s*(-?\d+)\s*\)")
_SIZE = re.compile(r"SIZE\s*\(\s*(\d+)\s*\.\.\s*(\d+)\s*\)", re.I)


def _int_val(value) -> int:
    return int(value.prettyPrint())


def validate_value(syntax: str, value) -> None:
    """Raise ValueError if value is wrong type or out of MIB range."""
    syntax_u = re.sub(r"\s+", " ", syntax.strip())
    syntax_l = syntax_u.lower()
    tname = type(value).__name__

    if syntax_l.startswith("counter"):
        if tname != "Counter32":
            raise ValueError(f"expected Counter32, got {tname}")
        v = _int_val(value)
        if not 0 <= v <= 4294967295:
            raise ValueError(f"Counter32 out of range: {v}")
        return

    if syntax_l.startswith("gauge"):
        if tname != "Gauge32":
            raise ValueError(f"expected Gauge32, got {tname}")
        v = _int_val(value)
        if not 0 <= v <= 4294967295:
            raise ValueError(f"Gauge32 out of range: {v}")
        return

    enums = [int(x.group(1)) for x in _ENUM.finditer(syntax_u)]
    if enums and ("integer" in syntax_l or syntax_u.upper().startswith("INTEGER")):
        if tname != "Integer32":
            raise ValueError(f"expected Integer32 for enum, got {tname}")
        v = _int_val(value)
        if v not in enums:
            raise ValueError(f"enum {v} not in {enums}")
        return

    rng = _RANGE.search(syntax_u)
    if rng and (syntax_l.startswith("integer") or syntax_u.upper().startswith("INTEGER")):
        lo, hi = int(rng.group(1)), int(rng.group(2))
        if hi > 2147483647:
            if tname != "Gauge32":
                raise ValueError(f"expected Gauge32 for large INTEGER, got {tname}")
        else:
            if tname != "Integer32":
                raise ValueError(f"expected Integer32, got {tname}")
        v = _int_val(value)
        if not lo <= v <= hi:
            raise ValueError(f"{v} not in {lo}..{hi}")
        return

    if "octet" in syntax_l or "displaystring" in syntax_l or "ownerstring" in syntax_l:
        if tname != "OctetString":
            raise ValueError(f"expected OctetString, got {tname}")
        size = _SIZE.search(syntax_u)
        n = len(bytes(value))
        if size:
            lo, hi = int(size.group(1)), int(size.group(2))
            if not lo <= n <= hi:
                raise ValueError(f"octet length {n} not in {lo}..{hi}")
        return

    if syntax_l.startswith("object identifier"):
        if tname != "ObjectIdentifier":
            raise ValueError(f"expected ObjectIdentifier, got {tname}")
        return

    # fallback: must prettyPrint
    if value.prettyPrint() is None:
        raise ValueError("value has no prettyPrint")
