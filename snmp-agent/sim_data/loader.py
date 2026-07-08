"""Load optional default_data.yaml overrides onto OID value store."""
from __future__ import annotations

from pathlib import Path

from pysnmp.proto import rfc1902

from value_factory import wrap_int_for_syntax


def _oid_from_dotted(text: str) -> tuple[int, ...]:
    return tuple(int(x) for x in text.strip().split("."))


def _value_from_spec(spec: object, syntax: str | None = None):
    if isinstance(spec, bool):
        return rfc1902.Integer32(1 if spec else 0)
    if isinstance(spec, int):
        if syntax:
            return wrap_int_for_syntax(spec, syntax)
        if spec > 2147483647:
            return rfc1902.Gauge32(spec)
        return rfc1902.Integer32(spec)
    if isinstance(spec, str):
        if spec.startswith("oid:"):
            return rfc1902.ObjectIdentifier(_oid_from_dotted(spec[4:]))
        return rfc1902.OctetString(spec.encode("ascii"))
    raise TypeError(f"unsupported override value: {spec!r}")


def apply_overrides(
    values: dict[tuple[int, ...], object],
    path: Path,
    oid_by_name: dict[str, tuple[int, ...]],
    syntax_by_name: dict[str, str] | None = None,
) -> None:
    try:
        import yaml
    except ImportError:
        return

    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    for oid_text, spec in (data.get("oids") or {}).items():
        key = _oid_from_dotted(oid_text)
        values[key] = _value_from_spec(spec)

    for name, spec in (data.get("scalars") or {}).items():
        if name not in oid_by_name:
            continue
        key = oid_by_name[name] + (0,)
        syntax = (syntax_by_name or {}).get(name)
        values[key] = _value_from_spec(spec, syntax)
