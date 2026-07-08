#!/usr/bin/env python3
"""Self-test all NTCIP 1202 (1202v0218.mib) OID default values and write report."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

_AGENT_ROOT = Path(__file__).resolve().parent.parent
MIBS = _AGENT_ROOT.parent / "mibs" / "mibs_old"
DEPS = _AGENT_ROOT / "deps"
REPORT_DIR = _AGENT_ROOT.parent / "reports"
REPORT_PATH = REPORT_DIR / "1202-selftest-report.md"

sys.path.insert(0, str(_AGENT_ROOT))

from mib_loader import DEFAULT_KNOWN, MIB_LOAD_ORDER, MibLoader  # noqa: E402
from instrum import FlatMibInstrum  # noqa: E402
from oid_utils import DEVICES_OID_ROOT, ASC_OID_ROOT  # noqa: E402
from pysnmp.proto import rfc1902  # noqa: E402
from sim_data.mib_syntax import load_full_syntax_map  # noqa: E402
from sim_data.validate import validate_value  # noqa: E402
from smi_parser import ParsedMib, merge_parsed, parse_mib_file  # noqa: E402

DEV_CAP = 3
MIB_FILE = "1202v0218.mib"

SPOT_CHECKS: list[tuple[str, tuple[int, ...], str | None]] = [
    ("maxPhases", (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 1, 0), "255"),
    ("phaseNumber.1", (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 1, 1), "1"),
    ("phasePedestrianClear.1", (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 3, 1), "255"),
    ("phaseRedClear.1 (col 1.9)", (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 9, 1), "255"),
    ("phaseRedRevert.1 (col 1.10)", (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 10, 1), "255"),
    ("preemptControl.1 DEFVAL 0", (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 6, 2, 1, 2, 1), "0"),
    ("preemptMinimumGreen.1 DEFVAL 255", (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 6, 2, 1, 6, 1), "255"),
    ("preemptDwellGreen.1 DEFVAL 10", (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 6, 2, 1, 10, 1), "10"),
    ("preemptTrackPhase.1 DEFVAL empty", (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 6, 2, 1, 12, 1), ""),
    ("splitMode enum max", (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 4, 1, 0), None),
]


def _names_1202() -> set[str]:
    merged = ParsedMib(oid_by_name=dict(DEFAULT_KNOWN))
    before: set[str] = set()
    for name in MIB_LOAD_ORDER:
        if name == MIB_FILE:
            break
        path = MIBS / name
        if not path.is_file():
            path = DEPS / name
        if not path.is_file():
            continue
        extra = parse_mib_file(str(path), merged.oid_by_name)
        merged = merge_parsed(merged, extra)
        before |= set(extra.objects)
    parsed = parse_mib_file(str(MIBS / MIB_FILE), merged.oid_by_name)
    return {n for n in parsed.objects if n not in before}


def _oid_str(oid: tuple[int, ...]) -> str:
    return ".".join(str(x) for x in oid)


def run_selftest() -> dict:
    names = _names_1202()
    full_syntax = load_full_syntax_map(MIBS, DEPS)
    loader = MibLoader(MIBS, dev_cap=DEV_CAP, oid_root=DEVICES_OID_ROOT)
    vals = loader.load()
    parsed = loader.parsed
    instrum = FlatMibInstrum(vals)

    results = {
        "missing": [],
        "invalid": [],
        "bogus_scalars": [],
        "spot_fail": [],
        "get_fail": [],
        "tables": [],
        "passed": True,
    }

    column_oids: set[tuple[int, ...]] = set()
    for table in parsed.tables:
        if table.name not in names:
            continue
        for col in table.columns:
            column_oids.add(table.base_oid + col.oid_suffix)
    for inst in parsed.scalars:
        if inst[-1] == 0 and inst[:-1] in column_oids:
            results["bogus_scalars"].append(_oid_str(inst))

    checked = 0
    for inst, obj in parsed.scalars.items():
        if obj.name not in names or obj.access == "not-accessible":
            continue
        if inst not in vals:
            results["missing"].append(f"scalar {obj.name}")
        else:
            checked += 1
            syn = full_syntax.get(obj.name, obj.syntax)
            try:
                validate_value(syn, vals[inst])
            except ValueError as exc:
                results["invalid"].append(f"{obj.name}: {exc}")

    for table in parsed.tables:
        if table.name not in names:
            continue
        rows = set()
        cols_ok = 0
        for col in table.columns:
            if col.access == "not-accessible":
                continue
            prefix = table.base_oid + col.oid_suffix
            matches = [k for k in vals if k[: len(prefix)] == prefix]
            if not matches:
                results["missing"].append(f"{table.name}.{col.name}")
                continue
            cols_ok += 1
            checked += 1
            for k in matches:
                rows.add(k[len(prefix) :])
            syn = full_syntax.get(col.name, col.syntax)
            try:
                validate_value(syn, vals[matches[0]])
            except ValueError as exc:
                results["invalid"].append(f"{table.name}.{col.name}: {exc}")
        results["tables"].append((table.name, len(rows), cols_ok))

    for label, oid, expected in SPOT_CHECKS:
        v = vals.get(oid)
        if v is None:
            results["spot_fail"].append(f"{label}: MISSING {_oid_str(oid)}")
            continue
        got = v.prettyPrint()
        if expected is not None and got != expected:
            results["spot_fail"].append(f"{label}: expected {expected!r}, got {got!r}")

    get_cases = [
        ("phaseRedRevert col", (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 10)),
        ("phaseNumber col", (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 1)),
    ]
    for label, col_oid in get_cases:
        resp = instrum.readVars([(rfc1902.ObjectName(col_oid), None)])[0]
        if resp[1].__class__.__name__ == "noSuchObject":
            results["get_fail"].append(f"{label}: noSuchObject")
        elif not resp[1].prettyPrint():
            results["get_fail"].append(f"{label}: empty value")

    results["checked"] = checked
    results["names_count"] = len(names)
    results["asc_instances"] = sum(1 for k in vals if k[: len(ASC_OID_ROOT)] == ASC_OID_ROOT)
    results["passed"] = not any(
        [
            results["missing"],
            results["invalid"],
            results["bogus_scalars"],
            results["spot_fail"],
            results["get_fail"],
        ]
    )
    return results


def write_report(results: dict) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    status = "PASS" if results["passed"] else "FAIL"

    lines = [
        "# NTCIP 1202 自测报告",
        "",
        f"- **时间**: {ts}",
        f"- **MIB**: `mibs/mibs_old/1202v0218.mib`",
        f"- **OID 范围**: `1.3.6.1.4.1.1206.4.2.1` (asc)",
        f"- **dev_cap**: {DEV_CAP}",
        f"- **结果**: **{status}**",
        "",
        "## 1. 汇总",
        "",
        "| 指标 | 值 |",
        "|---|---|",
        f"| 1202 定义对象数 | {results['names_count']} |",
        f"| 校验单元格数 | {results['checked']} |",
        f"| ASC 实例 OID 总数 | {results['asc_instances']} |",
        f"| 缺失 | {len(results['missing'])} |",
        f"| 类型/范围错误 | {len(results['invalid'])} |",
        f"| 错误 table-column scalar (.0) | {len(results['bogus_scalars'])} |",
        f"| 抽样失败 | {len(results['spot_fail'])} |",
        f"| Get 失败 | {len(results['get_fail'])} |",
        "",
        "## 2. 默认值规则",
        "",
        "| 类型 | 规则 |",
        "|---|---|",
        "| INTEGER (lo..hi) | 取 hi；INDEX 列取行号 |",
        "| INTEGER { enum } | 取最大 enum 值 |",
        "| DEFVAL | 优先使用 MIB DEFVAL |",
        "| Counter / Gauge | Counter32 / Gauge32 |",
        "| OCTET STRING | DEFVAL `\"\"` → 空串；否则按 SIZE |",
        "",
        "## 3. 表展开 (dev_cap={})".format(DEV_CAP),
        "",
        "| 表名 | 行数 | 可访问列数 |",
        "|---|---|---|",
    ]
    for name, rows, cols in sorted(results["tables"]):
        lines.append(f"| `{name}` | {rows} | {cols} |")

    lines.extend(["", "## 4. 抽样 OID 验证", "", "| 对象 | OID | 期望值 |", "|---|---|---|"])
    for label, oid, expected in SPOT_CHECKS:
        lines.append(f"| {label} | `{_oid_str(oid)}` | {expected if expected is not None else '(enum max)'} |")

    if results["spot_fail"]:
        lines.extend(["", "### 抽样失败", ""] + [f"- {x}" for x in results["spot_fail"]])

    if results["missing"]:
        lines.extend(["", "## 5. 缺失对象", ""] + [f"- {x}" for x in results["missing"][:30]])
    if results["invalid"]:
        lines.extend(["", "## 6. 类型/范围错误", ""] + [f"- {x}" for x in results["invalid"][:30]])
    if results["bogus_scalars"]:
        lines.extend(["", "## 7. 错误 scalar (.0)", ""] + [f"- `{x}`" for x in results["bogus_scalars"][:20]])

    lines.extend(
        [
            "",
            "## 8. phaseTable 列 OID 对照",
            "",
            "| 列后缀 | 对象名 |",
            "|---|---|",
            "| 1.9 | phaseRedClear |",
            "| 1.10 | **phaseRedRevert** |",
            "",
            "完整实例 = 表 OID + 列后缀 + 行号，例如 phaseRedRevert 第1行：`…1.1.2.1.10.1`",
            "",
            "## 9. 复现命令",
            "",
            "```bash",
            "cd test-agent/snmp-agent",
            "py scripts/selftest_1202.py",
            "py -m pytest tests/ -q",
            "```",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    return REPORT_PATH


def main() -> int:
    results = run_selftest()
    path = write_report(results)
    print(f"Report: {path}")
    print(f"Status: {'PASS' if results['passed'] else 'FAIL'}")
    print(f"Checked: {results['checked']}, missing: {len(results['missing'])}, invalid: {len(results['invalid'])}")
    return 0 if results["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
