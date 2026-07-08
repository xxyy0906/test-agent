"""Parse SMIv1 MIB source files into symbols, tables, and scalars."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

_M = re.MULTILINE
OID_ASSIGN_RE = re.compile(
    r"^(\S+)\s+OBJECT\s+IDENTIFIER\s*::=\s*\{\s*([^}]+)\s*\}",
    re.IGNORECASE | _M,
)
OBJECT_TYPE_START_RE = re.compile(r"^(\S+)\s+OBJECT-TYPE\s*$", re.IGNORECASE | _M)
OID_SUFFIX_RE = re.compile(r"::=\s*\{\s*([^}]+)\s*\}\s*$", re.IGNORECASE)
SYNTAX_RE = re.compile(r"^\s*SYNTAX\s+(.+)$", re.IGNORECASE)
ACCESS_RE = re.compile(r"^\s*ACCESS\s+(\S+)", re.IGNORECASE)
INDEX_RE = re.compile(r"^\s*INDEX\s*\{\s*([^}]+)\s*\}", re.IGNORECASE)
DEFVAL_RE = re.compile(r"^\s*DEFVAL\s*\{\s*([^}]+)\s*\}", re.IGNORECASE)
SEQ_OF_RE = re.compile(r"SEQUENCE\s+OF\s+(\S+)", re.IGNORECASE)
INT_RANGE_RE = re.compile(r"\(\s*(-?\d+)\s*\.\.\s*(-?\d+)\s*\)")


@dataclass
class MibObject:
    name: str
    oid: tuple[int, ...]
    syntax: str = ""
    access: str = "read-only"
    defval: str = ""
    indexes: list[str] = field(default_factory=list)
    is_table: bool = False
    is_entry: bool = False
    parent_table: str | None = None


@dataclass
class ColumnDef:
    name: str
    oid_suffix: tuple[int, ...]
    syntax: str
    access: str
    is_index: bool
    defval: str = ""


@dataclass
class TableDef:
    name: str
    base_oid: tuple[int, ...]
    entry_oid: tuple[int, ...]
    columns: list[ColumnDef] = field(default_factory=list)
    index_names: list[str] = field(default_factory=list)


@dataclass
class ParsedMib:
    objects: dict[str, MibObject] = field(default_factory=dict)
    scalars: dict[tuple[int, ...], MibObject] = field(default_factory=dict)
    tables: list[TableDef] = field(default_factory=list)
    oid_by_name: dict[str, tuple[int, ...]] = field(default_factory=dict)


def _strip_comments(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines():
        if "--" in line:
            line = line[: line.index("--")]
        out.append(line.rstrip())
    return "\n".join(out)


def _parse_oid_path(spec: str, known: dict[str, tuple[int, ...]]) -> tuple[int, ...]:
    parts = spec.replace(",", " ").split()
    if not parts:
        raise ValueError(f"empty OID path: {spec!r}")
    head = parts[0]
    if head not in known:
        raise KeyError(f"unknown OID symbol: {head}")
    oid = list(known[head])
    for token in parts[1:]:
        oid.append(int(token))
    return tuple(oid)


def _relative_suffix(base: tuple[int, ...], full: tuple[int, ...]) -> tuple[int, ...]:
    if full[: len(base)] != base:
        raise ValueError(f"{full} is not under {base}")
    return full[len(base) :]


def _syntax_max_int(syntax: str) -> int | None:
    m = INT_RANGE_RE.search(syntax)
    if not m:
        return None
    return int(m.group(2))


def parse_mib_file(path: str, known_oids: dict[str, tuple[int, ...]] | None = None) -> ParsedMib:
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = _strip_comments(fh.read())

    known = dict(known_oids or {})
    result = ParsedMib(oid_by_name=dict(known))

    for m in OID_ASSIGN_RE.finditer(text):
        name, spec = m.group(1), m.group(2).strip()
        oid = _parse_oid_path(spec, known)
        known[name] = oid
        result.oid_by_name[name] = oid
        obj = MibObject(name=name, oid=oid)
        result.objects[name] = obj

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = OBJECT_TYPE_START_RE.match(lines[i].strip())
        if not m:
            i += 1
            continue

        name = m.group(1)
        block: list[str] = []
        i += 1
        while i < len(lines):
            block.append(lines[i])
            if OID_SUFFIX_RE.search(lines[i]):
                break
            i += 1

        syntax = ""
        access = "read-only"
        defval = ""
        indexes: list[str] = []
        oid_suffix_spec = ""
        for bl in block:
            sm = SYNTAX_RE.match(bl)
            if sm:
                syntax = sm.group(1).strip()
                continue
            am = ACCESS_RE.match(bl)
            if am:
                access = am.group(1).lower()
                continue
            im = INDEX_RE.match(bl)
            if im:
                indexes = [x.strip() for x in im.group(1).replace(",", " ").split()]
                continue
            dm = DEFVAL_RE.match(bl)
            if dm:
                defval = dm.group(1).strip()
                continue
            om = OID_SUFFIX_RE.search(bl)
            if om:
                oid_suffix_spec = om.group(1).strip()

        if not oid_suffix_spec:
            i += 1
            continue

        oid = _parse_oid_path(oid_suffix_spec, known)
        known[name] = oid
        result.oid_by_name[name] = oid

        is_table = bool(SEQ_OF_RE.search(syntax))
        is_entry = bool(indexes) and not is_table

        obj = MibObject(
            name=name,
            oid=oid,
            syntax=syntax,
            access=access,
            defval=defval,
            indexes=indexes,
            is_table=is_table,
            is_entry=is_entry,
        )
        result.objects[name] = obj

        if is_table:
            entry_oid = oid + (1,)
            table = TableDef(name=name, base_oid=oid, entry_oid=entry_oid, index_names=[])
            result.tables.append(table)
        elif access != "not-accessible" and not is_entry:
            inst = oid + (0,)
            result.scalars[inst] = obj

        i += 1

    _wire_table_columns(result)
    _remove_table_column_scalars(result)
    return result


def _remove_table_column_scalars(parsed: ParsedMib) -> None:
    """Table columns are not scalars; drop erroneous oid+(.0,) entries."""
    column_oids: set[tuple[int, ...]] = set()
    for table in parsed.tables:
        for col in table.columns:
            column_oids.add(table.base_oid + col.oid_suffix)
    for inst in list(parsed.scalars):
        if inst[-1] == 0 and inst[:-1] in column_oids:
            del parsed.scalars[inst]


def _wire_table_columns(parsed: ParsedMib) -> None:
    table_by_entry_prefix: dict[tuple[int, ...], TableDef] = {}
    for table in parsed.tables:
        table_by_entry_prefix[table.entry_oid] = table

    for obj in parsed.objects.values():
        if obj.is_entry:
            table = table_by_entry_prefix.get(obj.oid)
            if table:
                table.index_names = list(obj.indexes)
            continue

        for table in parsed.tables:
            if obj.oid[: len(table.entry_oid)] != table.entry_oid:
                continue
            if obj.access == "not-accessible" and obj.name not in table.index_names:
                continue
            suffix = _relative_suffix(table.base_oid, obj.oid)
            is_index = obj.name in table.index_names
            table.columns.append(
                ColumnDef(
                    name=obj.name,
                    oid_suffix=suffix,
                    syntax=obj.syntax,
                    access=obj.access,
                    is_index=is_index,
                    defval=obj.defval,
                )
            )
            break


def merge_parsed(base: ParsedMib, extra: ParsedMib) -> ParsedMib:
    merged = ParsedMib(
        objects=dict(base.objects),
        scalars=dict(base.scalars),
        tables=list(base.tables),
        oid_by_name=dict(base.oid_by_name),
    )
    merged.objects.update(extra.objects)
    merged.scalars.update(extra.scalars)
    merged.tables.extend(extra.tables)
    merged.oid_by_name.update(extra.oid_by_name)
    return merged


def index_limit_from_syntax(syntax: str, fallback: int = 255) -> int:
    mx = _syntax_max_int(syntax)
    return mx if mx is not None else fallback
