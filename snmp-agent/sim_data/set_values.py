"""Generate alternate SNMP values for Set / read-back testing."""
from __future__ import annotations

import re
from dataclasses import dataclass

from pysnmp.proto import rfc1902

from oid_registry import OidMeta
from value_factory import NTCIP_DEFAULT_OID, wrap_int_for_syntax

_ENUM = re.compile(r"\(\s*(-?\d+)\s*\)")
_RANGE = re.compile(r"\(\s*(-?\d+)\s*\.\.\s*(-?\d+)\s*\)")
_SIZE = re.compile(r"SIZE\s*\(\s*(\d+)\s*\.\.\s*(\d+)\s*\)", re.I)


@dataclass(frozen=True)
class SetTestCase:
    name: str
    syntax: str
    instance_oid: tuple[int, ...]
    access: str


def _int_from_val(val) -> int:
    return int(val.prettyPrint())


def _enums(syntax: str) -> list[int]:
    return [int(m.group(1)) for m in _ENUM.finditer(syntax)]


def _range_bounds(syntax: str) -> tuple[int, int] | None:
    m = _RANGE.search(syntax)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def _size_bounds(syntax: str) -> tuple[int, int] | None:
    m = _SIZE.search(syntax)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def pick_representative_oid(name: str, oids: list[tuple[int, ...]]) -> tuple[int, ...]:
    """Prefer row 1.1 (dual index) or row 1 for table instances."""
    if not oids:
        raise ValueError(f"no instances for {name}")
    for oid in sorted(oids):
        if len(oid) >= 2 and oid[-2:] == (1, 1):
            return oid
    for oid in sorted(oids):
        if oid[-1] == 1:
            return oid
    return sorted(oids)[0]


def collect_writable_set_cases(
    registry: dict[tuple[int, ...], OidMeta],
) -> list[SetTestCase]:
    by_name: dict[str, list[tuple[int, ...]]] = {}
    meta_by_name: dict[str, OidMeta] = {}
    for oid, meta in registry.items():
        if not meta.is_writable:
            continue
        by_name.setdefault(meta.name, []).append(oid)
        meta_by_name[meta.name] = meta

    cases: list[SetTestCase] = []
    for name in sorted(by_name):
        meta = meta_by_name[name]
        inst = pick_representative_oid(name, by_name[name])
        cases.append(
            SetTestCase(
                name=name,
                syntax=meta.syntax,
                instance_oid=inst,
                access=meta.access,
            )
        )
    return cases


def collect_readonly_negative_samples(
    registry: dict[tuple[int, ...], OidMeta],
    limit: int = 20,
) -> list[SetTestCase]:
    by_name: dict[str, list[tuple[int, ...]]] = {}
    meta_by_name: dict[str, OidMeta] = {}
    for oid, meta in registry.items():
        if meta.is_writable or meta.access != "read-only":
            continue
        by_name.setdefault(meta.name, []).append(oid)
        meta_by_name[meta.name] = meta

    cases: list[SetTestCase] = []
    for name in sorted(by_name):
        if len(cases) >= limit:
            break
        meta = meta_by_name[name]
        inst = pick_representative_oid(name, by_name[name])
        cases.append(
            SetTestCase(
                name=name,
                syntax=meta.syntax,
                instance_oid=inst,
                access=meta.access,
            )
        )
    return cases


def _set_int_value(syntax_u: str, syntax_l: str, new_n: int):
    """Pick SNMP type for Set: Gauge32 for non-negative, Integer32 if range allows negative."""
    rng = _range_bounds(syntax_u)
    if rng and rng[0] < 0:
        return rfc1902.Integer32(new_n)
    return rfc1902.Gauge32(new_n)


def alternate_set_value(syntax: str, current) -> object:
    """Return a MIB-valid value different from *current*."""
    syntax_u = re.sub(r"\s+", " ", syntax.strip())
    syntax_l = syntax_u.lower()
    tname = type(current).__name__

    if syntax_l.startswith("counter") or syntax_u.startswith("Counter"):
        cur = _int_from_val(current) if tname == "Counter32" else 0
        new_n = 0 if cur != 0 else 1
        return rfc1902.Counter32(new_n)

    if syntax_l.startswith("gauge") or syntax_u.startswith("Gauge"):
        cur = _int_from_val(current)
        new_n = 0 if cur != 0 else 1
        return rfc1902.Gauge32(new_n)

    enums = _enums(syntax_u)
    if enums and ("integer" in syntax_l or syntax_u.upper().startswith("INTEGER")):
        cur = _int_from_val(current)
        for e in sorted(enums):
            if e != cur:
                return _set_int_value(syntax_u, syntax_l, e)
        return _set_int_value(syntax_u, syntax_l, enums[0])

    rng = _range_bounds(syntax_u)
    if rng and (syntax_l.startswith("integer") or syntax_u.upper().startswith("INTEGER")):
        lo, hi = rng
        cur = _int_from_val(current)
        if cur != lo:
            new_n = lo
        elif hi != lo:
            new_n = lo + 1 if lo + 1 <= hi else hi - 1
        else:
            new_n = lo
        if lo < 0:
            return rfc1902.Integer32(new_n)
        return _set_int_value(syntax_u, syntax_l, new_n)

    if any(x in syntax_l for x in ("octet", "displaystring", "ownerstring", "oerstring", "bitmap")):
        lo, hi = _size_bounds(syntax_u) or (0, 255)
        alt = b"SET"
        if lo > len(alt):
            alt = b"A" * lo
        if len(alt) > hi:
            alt = alt[:hi]
        cur = bytes(current) if tname == "OctetString" else b""
        if alt == cur and hi >= lo + 1:
            alt = b"B" * max(lo, 1)
        return rfc1902.OctetString(alt)

    if syntax_l.startswith("object identifier") or syntax_u.startswith("OBJECT IDENTIFIER"):
        alt_oid = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 1, 0)
        if tuple(int(x) for x in current.prettyPrint().split(".")) == alt_oid:
            alt_oid = NTCIP_DEFAULT_OID
        return rfc1902.ObjectIdentifier(alt_oid)

    cur = _int_from_val(current)
    new_n = 0 if cur != 0 else 1
    return _set_int_value(syntax_u, syntax_l, new_n)


def invalid_set_value(syntax: str, current) -> object:
    """Return a value that should fail SYNTAX validation."""
    syntax_u = re.sub(r"\s+", " ", syntax.strip())
    syntax_l = syntax_u.lower()

    enums = _enums(syntax_u)
    if enums:
        bad = max(enums) + 100
        return rfc1902.Integer32(bad)

    rng = _range_bounds(syntax_u)
    if rng and (syntax_l.startswith("integer") or syntax_u.upper().startswith("INTEGER")):
        lo, hi = rng
        if hi >= 4294967295 or hi > 2147483647:
            return rfc1902.Integer32(-1)
        bad_n = hi + 999
        if bad_n > hi:
            return wrap_int_for_syntax(bad_n, syntax_u)
        if lo > 0:
            return wrap_int_for_syntax(lo - 1, syntax_u)
        return rfc1902.Integer32(-1)

    size = _size_bounds(syntax_u)
    if size and any(x in syntax_l for x in ("octet", "displaystring", "ownerstring")):
        _, hi = size
        return rfc1902.OctetString(b"X" * (hi + 1))

    if syntax_l.startswith("counter"):
        return rfc1902.Integer32(999999)

    if syntax_l.startswith("object identifier") or syntax_u.startswith("OBJECT IDENTIFIER"):
        return rfc1902.Integer32(1)

    if syntax_l.startswith("integer") or syntax_u.upper().startswith("INTEGER"):
        # Unconstrained INTEGER — reject via wrong ASN.1 type
        return rfc1902.OctetString(b"bad")

    return rfc1902.Integer32(999999)
