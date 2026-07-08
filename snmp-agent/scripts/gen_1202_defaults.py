#!/usr/bin/env python3
"""Generate full 1202 MIB object default-value listing (253 objects, by OID)."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

_AGENT_ROOT = Path(__file__).resolve().parent.parent
_TEST_AGENT = _AGENT_ROOT.parent
MIBS = _TEST_AGENT / "mibs" / "mibs_old"
DEPS = _AGENT_ROOT / "deps"
DOCS = _TEST_AGENT / "docs"
OUT_MD = DOCS / "1202DEFAULT_DATA-OIDs.md"
OUT_CSV = DOCS / "1202DEFAULT_DATA-OIDs.csv"

sys.path.insert(0, str(_AGENT_ROOT))

from mib_loader import DEFAULT_KNOWN, MIB_LOAD_ORDER, MibLoader  # noqa: E402
from oid_utils import ASC_OID_ROOT  # noqa: E402
from sim_data.mib_syntax import load_full_syntax_map  # noqa: E402
from smi_parser import ParsedMib, merge_parsed, parse_mib_file  # noqa: E402


def _oid_str(oid: tuple[int, ...]) -> str:
    return ".".join(str(x) for x in oid)


def _names_1202() -> set[str]:
    merged = ParsedMib(oid_by_name=dict(DEFAULT_KNOWN))
    before: set[str] = set()
    for name in MIB_LOAD_ORDER:
        if name == "1202v0218.mib":
            break
        path = MIBS / name
        if not path.is_file():
            path = DEPS / name
        if not path.is_file():
            continue
        extra = parse_mib_file(str(path), merged.oid_by_name)
        merged = merge_parsed(merged, extra)
        before |= set(extra.objects)
    parsed = parse_mib_file(str(MIBS / "1202v0218.mib"), merged.oid_by_name)
    return {n for n in parsed.objects if n not in before}


def _format_value(val, max_len: int = 48) -> str:
    if val is None:
        return "—"
    t = type(val).__name__
    if t == "OctetString":
        raw = bytes(val)
        if not raw:
            return '""'
        try:
            text = raw.decode("ascii")
            if all(32 <= ord(c) < 127 or c in "\r\n\t" for c in text):
                s = repr(text)
                if len(s) > max_len:
                    return f"{s[: max_len - 3]}... ({len(raw)} bytes)"
                return s
        except UnicodeDecodeError:
            pass
        hx = raw.hex()
        if len(hx) > max_len:
            return f"{hx[: max_len - 3]}... ({len(raw)} bytes)"
        return hx
    if t == "ObjectIdentifier":
        return _oid_str(tuple(int(x) for x in val.prettyPrint().split(".")))
    s = val.prettyPrint()
    if len(s) > max_len:
        return s[: max_len - 3] + "..."
    return s


def _collect_rows() -> list[dict]:
    names = _names_1202()
    loader = MibLoader(MIBS, dev_cap=1, oid_root=ASC_OID_ROOT)
    vals = loader.load()
    parsed = loader.parsed
    full_syntax = load_full_syntax_map(MIBS, DEPS)

    rows: list[dict] = []
    seen: set[str] = set()

    def add(name: str, kind: str, def_oid: tuple[int, ...], inst_oid, access: str, syntax: str, value: str):
        if name in seen:
            return
        seen.add(name)
        rows.append(
            {
                "name": name,
                "kind": kind,
                "def_oid": _oid_str(def_oid),
                "inst_oid": _oid_str(inst_oid) if inst_oid else "—",
                "access": access,
                "syntax": syntax.replace("\n", " ").strip()[:120],
                "default": value,
            }
        )

    for inst, obj in sorted(parsed.scalars.items(), key=lambda x: x[0]):
        if obj.name not in names:
            continue
        syn = full_syntax.get(obj.name, obj.syntax)
        if obj.access == "not-accessible":
            add(obj.name, "branch/entry", obj.oid, None, obj.access, syn, "—")
        else:
            v = vals.get(inst)
            add(obj.name, "scalar", obj.oid, inst, obj.access, syn, _format_value(v))

    for table in parsed.tables:
        if table.name not in names:
            continue
        syn = full_syntax.get(table.name, "SEQUENCE OF")
        add(table.name, "table", table.base_oid, None, "not-accessible", syn, "—")
        entry_name = next((n for n, o in parsed.objects.items() if o.is_entry and o.parent_table == table.name), f"{table.name}Entry")
        if entry_name in names:
            entry = parsed.objects[entry_name]
            add(entry_name, "entry", entry.oid, None, "not-accessible", entry.syntax or "ROW", "—")

        for col in table.columns:
            if col.name not in names:
                continue
            col_def = table.base_oid + col.oid_suffix
            syn = full_syntax.get(col.name, col.syntax)
            if col.access == "not-accessible":
                add(col.name, "column(index)", col_def, None, col.access, syn, "—")
                continue
            prefix = col_def
            matches = sorted(k for k in vals if k[: len(prefix)] == prefix and len(k) > len(prefix))
            inst = matches[0] if matches else None
            val = _format_value(vals[inst]) if inst else "—"
            add(col.name, "column", col_def, inst, col.access, syn, val)

    # Any 1202 objects not yet emitted (OBJECT IDENTIFIER branches etc.)
    for name in sorted(names):
        if name in seen:
            continue
        obj = parsed.objects[name]
        syn = full_syntax.get(name, obj.syntax)
        kind = "branch"
        if obj.is_table:
            kind = "table"
        elif obj.is_entry:
            kind = "entry"
        add(name, kind, obj.oid, None, obj.access, syn, "—")

    rows.sort(key=lambda r: r["def_oid"])
    return rows


def write_md(rows: list[dict]) -> None:
    lines = [
        "# 1202 全部对象默认值清单（按 OID）",
        "",
        "| 项 | 值 |",
        "|---|---|",
        f"| MIB | `mibs/mibs_old/1202v0218.mib` |",
        f"| 对象数 | **{len(rows)}** |",
        f"| OID 范围 | `1.3.6.1.4.1.1206.4.2.1` (asc) |",
        "| 表实例 | `dev_cap=1`（每列展示第 1 行实例 OID 与值） |",
        "| 规则 | 见 [1202DEFAULT_DATA.md](1202DEFAULT_DATA.md) |",
        "",
        "## 清单",
        "",
        "| # | 对象名 | 类型 | 定义 OID | 实例 OID (row 1) | ACCESS | 默认值 |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        syn_short = r["syntax"].replace("|", "\\|")
        if len(syn_short) > 60:
            syn_short = syn_short[:57] + "..."
        lines.append(
            f"| {i} | `{r['name']}` | {r['kind']} | `{r['def_oid']}` | `{r['inst_oid']}` | {r['access']} | {r['default']} |"
        )
    lines.extend(
        [
            "",
            "## 说明",
            "",
            "- **scalar**：实例 OID = 定义 OID + `.0`",
            "- **column**：Get 列 OID（无行号）时，自动补 table key 第 1 行（如 …8.2.1.1 → …8.2.1.1.1）；Agent 响应返回完整实例 OID",
            "- **table/entry/branch**：`not-accessible`，无 SNMP 实例值",
            "- 满填模式下每列另有 max* 行实例，完整树见 `tree/1202v0218-tree.md`",
            "",
            "重新生成：`py scripts/gen_1202_defaults.py`",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def write_csv(rows: list[dict]) -> None:
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["name", "kind", "def_oid", "inst_oid", "access", "syntax", "default"],
        )
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    rows = _collect_rows()
    DOCS.mkdir(parents=True, exist_ok=True)
    write_md(rows)
    write_csv(rows)
    print(f"Objects: {len(rows)}")
    print(f"Wrote: {OUT_MD}")
    print(f"Wrote: {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
