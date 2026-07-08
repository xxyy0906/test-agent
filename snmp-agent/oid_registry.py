"""Per-instance OID metadata (SYNTAX, ACCESS) for SNMP Set validation."""
from __future__ import annotations

from dataclasses import dataclass

from smi_parser import ParsedMib


@dataclass(frozen=True)
class OidMeta:
    name: str
    syntax: str
    access: str

    @property
    def is_writable(self) -> bool:
        return self.access in ("read-write", "read-create")


def build_oid_registry(
    parsed: ParsedMib,
    values: dict[tuple[int, ...], object],
    syntax_by_name: dict[str, str],
) -> dict[tuple[int, ...], OidMeta]:
    """Map every loaded instance OID to MIB object metadata."""
    registry: dict[tuple[int, ...], OidMeta] = {}

    for inst, obj in parsed.scalars.items():
        if inst not in values:
            continue
        registry[inst] = OidMeta(
            obj.name,
            syntax_by_name.get(obj.name, obj.syntax),
            obj.access,
        )

    table_prefixes: list[tuple[tuple[int, ...], OidMeta]] = []
    for table in parsed.tables:
        for col in table.columns:
            if col.access == "not-accessible" and col.name not in table.index_names:
                continue
            prefix = table.base_oid + col.oid_suffix
            meta = OidMeta(
                col.name,
                syntax_by_name.get(col.name, col.syntax),
                col.access,
            )
            table_prefixes.append((prefix, meta))

    for oid in values:
        if oid in registry:
            continue
        for prefix, meta in table_prefixes:
            if oid[: len(prefix)] == prefix and len(oid) > len(prefix):
                registry[oid] = meta
                break

    return registry
