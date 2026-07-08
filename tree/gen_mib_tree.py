#!/usr/bin/env python3
"""Generate OID tree with types/ranges for NTCIP MIB files."""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNMP_AGENT = ROOT / "snmp-agent"
sys.path.insert(0, str(SNMP_AGENT))

from mib_loader import DEFAULT_KNOWN, MIB_LOAD_ORDER  # noqa: E402
from smi_parser import ParsedMib, merge_parsed, parse_mib_file  # noqa: E402

MIB_DIR = ROOT / "mibs" / "mibs_old"
DEPS_DIR = SNMP_AGENT / "deps"

_ENUM = re.compile(r"(\w+)\s*\(\s*(-?\d+)\s*\)")
_RANGE = re.compile(r"\(\s*(-?\d+)\s*\.\.\s*(-?\d+)\s*\)")
_SIZE = re.compile(r"SIZE\s*\(\s*(\d+)\s*\.\.\s*(\d+)\s*\)", re.I)


@dataclass
class MibTreeConfig:
    mib_file: str
    stem: str
    title: str
    overview_md: str
    branch_prefixes: list[tuple[tuple[int, ...], str]] | None = None
    anchor_symbol: str | None = None  # group by next OID segment after anchor


@dataclass
class Node:
    name: str
    oid: tuple[int, ...]
    kind: str
    syntax: str = ""
    access: str = ""
    defval: str = ""
    type_desc: str = ""
    range_desc: str = ""
    children: list["Node"] = field(default_factory=list)


MIB_CONFIGS: dict[str, MibTreeConfig] = {
    "1201v0227.mib": MibTreeConfig(
        mib_file="1201v0227.mib",
        stem="1201v0227",
        title="NTCIP 1201 Global",
        overview_md="""```
1.3.6.1.4.1.1206
├── 4.1.2.3  profilesPMPP          (HDLC, 1201 §2.6)
└── 4.2.6    global (8004 devices.6)
    ├── 1  globalConfiguration
    ├── 2  globalDBManagement
    ├── 3  globalTimeManagement
    └── 7  auxIO
```""",
        branch_prefixes=[
            ((1, 3, 6, 1, 4, 1, 1206, 4, 2, 6, 1), "globalConfiguration (1.3.6.1.4.1.1206.4.2.6.1)"),
            ((1, 3, 6, 1, 4, 1, 1206, 4, 2, 6, 2), "globalDBManagement (1.3.6.1.4.1.1206.4.2.6.2)"),
            ((1, 3, 6, 1, 4, 1, 1206, 4, 2, 6, 3), "globalTimeManagement (1.3.6.1.4.1.1206.4.2.6.3)"),
            ((1, 3, 6, 1, 4, 1, 1206, 4, 1, 2, 3), "profilesPMPP (1.3.6.1.4.1.1206.4.1.2.3)"),
            ((1, 3, 6, 1, 4, 1, 1206, 4, 2, 6, 7), "auxIO (1.3.6.1.4.1.1206.4.2.6.7)"),
        ],
    ),
    "1202v0218.mib": MibTreeConfig(
        mib_file="1202v0218.mib",
        stem="1202v0218",
        title="NTCIP 1202 ASC",
        overview_md="""```
1.3.6.1.4.1.1206.4.2.1  asc (devices.1)
├── 1   phase           相位
├── 2   detector        检测器
├── 3   unit            单元/报警
├── 4   coord           协调/模式/配时
├── 5   timebaseAsc     时基动作
├── 6   preempt         优先
├── 7   ring            环/序列
├── 8   channel         通道
├── 9   overlap         重叠
├── 10  ts2port1        TS2 Port1
└── 11  ascBlock        ASC 块传输
```""",
        anchor_symbol="asc",
    ),
}


def _strip_comments(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines():
        if "--" in line:
            line = line[: line.index("--")]
        out.append(line.rstrip())
    return "\n".join(out)


def _load_full_syntax(mib_path: Path) -> dict[str, str]:
    text = _strip_comments(mib_path.read_text(encoding="utf-8", errors="replace"))
    result: dict[str, str] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(r"^(\S+)\s+OBJECT-TYPE\s*$", lines[i], re.I)
        if not m:
            i += 1
            continue
        name = m.group(1)
        i += 1
        syntax_parts: list[str] = []
        in_syntax = False
        while i < len(lines):
            line = lines[i]
            if re.match(r"^\s*SYNTAX\s+", line, re.I):
                in_syntax = True
                syntax_parts.append(re.sub(r"^\s*SYNTAX\s+", "", line, flags=re.I).strip())
                i += 1
                continue
            if in_syntax:
                if re.match(r"^\s*(ACCESS|STATUS|DESCRIPTION)\s", line, re.I):
                    break
                syntax_parts.append(line.strip())
            if re.search(r"::=\s*\{", line):
                break
            i += 1
        if syntax_parts:
            result[name] = " ".join(syntax_parts)
        i += 1
    return result


def _load_before(mib_file: str) -> ParsedMib:
    merged = ParsedMib(oid_by_name=dict(DEFAULT_KNOWN))
    for name in MIB_LOAD_ORDER:
        if name == mib_file:
            break
        path = MIB_DIR / name
        if not path.is_file():
            path = DEPS_DIR / name
        if not path.is_file():
            continue
        extra = parse_mib_file(str(path), merged.oid_by_name)
        merged = merge_parsed(merged, extra)
    return merged


def _names_from_mib(before: ParsedMib, parsed: ParsedMib) -> set[str]:
    return {n for n in parsed.objects if n not in before.objects}


def _describe_syntax(syntax: str) -> tuple[str, str]:
    if not syntax:
        return "OBJECT IDENTIFIER", "(branch node)"
    s = re.sub(r"\s+", " ", syntax.strip())
    sl = s.lower()

    if "sequence of" in sl:
        return "TABLE", s

    enums = _ENUM.findall(s)
    if enums and ("integer" in sl or s.upper().startswith("INTEGER")):
        vals = [int(v) for _, v in enums]
        lo, hi = min(vals), max(vals)
        items = ", ".join(f"{n}={v}" for n, v in enums)
        return "INTEGER (enum)", f"{lo} .. {hi}  ({items})"

    rng = _RANGE.search(s)
    size = _SIZE.search(s)

    if sl.startswith("counter"):
        return "Counter32", "0 .. 4294967295"
    if sl.startswith("gauge"):
        return "Gauge32", "0 .. 4294967295"
    if sl.startswith("object identifier"):
        return "OBJECT IDENTIFIER", "(any valid OID)"
    if "displaystring" in sl or "ownerstring" in sl:
        if size:
            return "DisplayString", f"length {size.group(1)} .. {size.group(2)} bytes"
        return "DisplayString", "length 0 .. 255 bytes"
    if "octet string" in sl:
        if size:
            return "OCTET STRING", f"length {size.group(1)} .. {size.group(2)} bytes"
        return "OCTET STRING", "length 0 .. 65535 bytes"
    if sl.startswith("integer"):
        if rng:
            hi = int(rng.group(2))
            lo = int(rng.group(1))
            if hi > 2147483647:
                return "Gauge32 (INTEGER range)", f"{lo} .. {hi}"
            return "INTEGER", f"{lo} .. {hi}"
        return "INTEGER", "-2147483648 .. 2147483647"
    if rng:
        return s.split()[0], f"{rng.group(1)} .. {rng.group(2)}"
    return s, "(see MIB SYNTAX)"


def _column_names(parsed: ParsedMib, names: set[str]) -> set[str]:
    cols: set[str] = set()
    for table in parsed.tables:
        if table.name not in names:
            continue
        for col in table.columns:
            cols.add(col.name)
    return cols


def _build_nodes(parsed: ParsedMib, names: set[str], full_syntax: dict[str, str]) -> list[Node]:
    col_names = _column_names(parsed, names)
    table_cols: dict[str, list[Node]] = {}
    for table in parsed.tables:
        if table.name not in names:
            continue
        cols = []
        for col in sorted(table.columns, key=lambda c: c.oid_suffix):
            syn = full_syntax.get(col.name, col.syntax)
            td, rd = _describe_syntax(syn)
            cols.append(
                Node(
                    name=col.name,
                    oid=table.base_oid + col.oid_suffix,
                    kind="column",
                    syntax=syn,
                    access=col.access,
                    defval=col.defval,
                    type_desc=td,
                    range_desc=rd + (" [INDEX]" if col.is_index else ""),
                )
            )
        table_cols[table.name] = cols

    nodes: list[Node] = []
    for name in sorted(names, key=lambda n: parsed.oid_by_name.get(n, ())):
        if name in col_names:
            continue
        obj = parsed.objects[name]
        syn = full_syntax.get(name, obj.syntax)
        td, rd = _describe_syntax(syn)
        if obj.is_table:
            kind = "table"
        elif obj.is_entry:
            kind = "entry"
            td = "ROW ENTRY"
            rd = f"INDEX {{ {', '.join(obj.indexes)} }}"
        elif syn:
            kind = "scalar"
        else:
            kind = "node"
            td, rd = "OBJECT IDENTIFIER", "(branch node)"

        n = Node(
            name=name,
            oid=obj.oid,
            kind=kind,
            syntax=syn,
            access=obj.access,
            defval=obj.defval,
            type_desc=td,
            range_desc=rd,
        )
        if obj.is_table and name in table_cols:
            n.children = table_cols[name]
        nodes.append(n)
    return nodes


def _format_oid(oid: tuple[int, ...]) -> str:
    return ".".join(str(x) for x in oid)


def _group_by_prefixes(nodes: list[Node], prefixes: list[tuple[tuple[int, ...], str]]) -> dict[str, list[Node]]:
    branches: dict[str, list[Node]] = {}
    for n in nodes:
        placed = False
        for prefix, label in prefixes:
            if n.oid[: len(prefix)] == prefix or n.oid == prefix:
                branches.setdefault(label, []).append(n)
                placed = True
                break
        if not placed:
            branches.setdefault("other", []).append(n)
    return branches


def _group_by_anchor(
    nodes: list[Node], anchor: tuple[int, ...], oid_by_name: dict[str, tuple[int, ...]]
) -> dict[str, list[Node]]:
    oid_to_name = {v: k for k, v in oid_by_name.items()}
    branches: dict[str, list[Node]] = {}
    order: list[str] = []

    for n in nodes:
        if n.oid == anchor:
            label = f"asc ({_format_oid(anchor)})"
        elif n.oid[: len(anchor)] != anchor:
            label = "other"
        elif len(n.oid) == len(anchor):
            label = f"asc ({_format_oid(anchor)})"
        else:
            seg = n.oid[len(anchor)]
            branch_oid = anchor + (seg,)
            bname = oid_to_name.get(branch_oid, f"branch{seg}")
            label = f"{bname} ({_format_oid(branch_oid)})"
        if label not in branches:
            branches[label] = []
            order.append(label)
        branches[label].append(n)

    return {k: branches[k] for k in order}


def _branch_order(branches: dict[str, list[Node]], config: MibTreeConfig) -> list[str]:
    if config.branch_prefixes:
        order = [label for _, label in config.branch_prefixes]
        if "other" in branches:
            order.append("other")
        return order
    return list(branches.keys())


def _render_node(n: Node, indent: int, lines: list[str]) -> None:
    prefix = "  " * indent
    oid_s = _format_oid(n.oid)
    if n.kind == "scalar":
        inst = f"{oid_s}.0"
    elif n.kind == "column":
        inst = f"{oid_s}.{{index...}}"
    else:
        inst = oid_s

    lines.append(f"{prefix}{n.name}")
    lines.append(f"{prefix}  OID: {oid_s}")
    lines.append(f"{prefix}  实例: {inst}")
    lines.append(f"{prefix}  类型: {n.type_desc}")
    lines.append(f"{prefix}  范围: {n.range_desc}")
    if n.access:
        lines.append(f"{prefix}  ACCESS: {n.access}")
    if n.defval:
        lines.append(f"{prefix}  DEFVAL: {{ {n.defval} }}")
    if n.syntax and n.kind not in ("node",):
        lines.append(f"{prefix}  SYNTAX: {n.syntax}")
    lines.append("")
    for child in n.children:
        _render_node(child, indent + 1, lines)


def generate_tree(config: MibTreeConfig, out_dir: Path | None = None) -> Path:
    out_dir = out_dir or Path(__file__).resolve().parent
    mib_path = MIB_DIR / config.mib_file
    before = _load_before(config.mib_file)
    parsed = parse_mib_file(str(mib_path), before.oid_by_name)
    names = _names_from_mib(before, parsed)
    full_syntax = _load_full_syntax(mib_path)
    nodes = _build_nodes(parsed, names, full_syntax)

    if config.branch_prefixes:
        branches = _group_by_prefixes(nodes, config.branch_prefixes)
    elif config.anchor_symbol:
        anchor = parsed.oid_by_name[config.anchor_symbol]
        branches = _group_by_anchor(nodes, anchor, parsed.oid_by_name)
    else:
        branches = {"all": nodes}

    branch_order = _branch_order(branches, config)
    stem = config.stem
    txt_path = out_dir / f"{stem}-tree.txt"
    md_path = out_dir / f"{stem}-tree.md"
    csv_path = out_dir / f"{stem}-flat.csv"

    lines = [
        "=" * 72,
        f"{config.title} — OID 树 / 类型 / 范围",
        "=" * 72,
        f"源文件: mibs/mibs_old/{config.mib_file}",
        f"对象总数: {len(names)}",
        "",
        "说明:",
        "  - scalar 实例 OID = 定义 OID + .0",
        "  - table 列实例 OID = 表 OID + 列后缀 + 索引",
        "",
    ]
    for label in branch_order:
        group = branches.get(label, [])
        if not group:
            continue
        lines.append("-" * 72)
        lines.append(label)
        lines.append("-" * 72)
        for n in sorted(group, key=lambda x: x.oid):
            _render_node(n, 0, lines)
    txt_path.write_text("\n".join(lines), encoding="utf-8")

    md = [
        f"# {config.title} — OID 树 / 类型 / 范围",
        "",
        "| 项 | 值 |",
        "|---|---|",
        f"| 源文件 | `mibs/mibs_old/{config.mib_file}` |",
        f"| 对象总数 | {len(names)} |",
        "",
        "## 分支概览",
        "",
        config.overview_md,
        "",
    ]
    for label in branch_order:
        group = branches.get(label, [])
        if not group:
            continue
        md.append(f"## {label}")
        md.append("")
        for n in sorted(group, key=lambda x: x.oid):
            md.append(f"### `{n.name}`")
            md.append("")
            md.append("| 属性 | 值 |")
            md.append("|---|---|")
            md.append(f"| OID | `{_format_oid(n.oid)}` |")
            md.append(f"| 类型 | {n.type_desc} |")
            md.append(f"| 范围 | {n.range_desc} |")
            if n.access:
                md.append(f"| ACCESS | {n.access} |")
            if n.defval:
                md.append(f"| DEFVAL | `{{ {n.defval} }}` |")
            if n.syntax:
                md.append(f"| SYNTAX | `{n.syntax}` |")
            md.append("")
            if n.children:
                md.append("**表列:**")
                md.append("")
                md.append("| 列名 | OID后缀 | 类型 | 范围 | ACCESS | DEFVAL | INDEX |")
                md.append("|---|---|---|---|---|---|---|")
                for c in n.children:
                    suffix = ".".join(str(x) for x in c.oid[len(n.oid) :])
                    md.append(
                        f"| `{c.name}` | `{suffix}` | {c.type_desc} | {c.range_desc} | "
                        f"{c.access} | `{c.defval}` | {'Y' if '[INDEX]' in c.range_desc else ''} |"
                    )
                md.append("")
    md_path.write_text("\n".join(md), encoding="utf-8")

    csv_lines = ["name,oid,kind,type,range,access,defval,syntax,parent_table"]
    for n in nodes:
        csv_lines.append(
            f'"{n.name}","{_format_oid(n.oid)}",{n.kind},"{n.type_desc}","{n.range_desc}",'
            f'"{n.access}","{n.defval}","{n.syntax.replace(chr(34), chr(39))}",""'
        )
        for c in n.children:
            csv_lines.append(
                f'"{c.name}","{_format_oid(c.oid)}",column,"{c.type_desc}","{c.range_desc}",'
                f'"{c.access}","{c.defval}","{c.syntax.replace(chr(34), chr(39))}","{n.name}"'
            )
    csv_path.write_text("\n".join(csv_lines), encoding="utf-8-sig")

    print(f"Wrote {txt_path}")
    print(f"Wrote {md_path}")
    print(f"Wrote {csv_path}")
    print(f"Objects: {len(names)}")
    return txt_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate MIB OID tree documentation")
    parser.add_argument(
        "mib",
        nargs="?",
        default="1201v0227.mib",
        help="MIB filename under mibs/mibs_old/ (e.g. 1202v0218.mib)",
    )
    args = parser.parse_args()
    if args.mib not in MIB_CONFIGS:
        stem = Path(args.mib).stem.split("v")[0]
        config = MibTreeConfig(
            mib_file=args.mib,
            stem=Path(args.mib).stem.replace(".", "-") if "." in args.mib else args.mib.replace(".mib", ""),
            title=args.mib,
            overview_md="(auto)",
            anchor_symbol=None,
        )
        # try common anchors
        before = _load_before(args.mib)
        parsed = parse_mib_file(str(MIB_DIR / args.mib), before.oid_by_name)
        for sym in ("asc", "global", "devices"):
            if sym in parsed.oid_by_name:
                config.anchor_symbol = sym
                break
    else:
        config = MIB_CONFIGS[args.mib]
    generate_tree(config)


if __name__ == "__main__":
    main()
