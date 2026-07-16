#!/usr/bin/env python3
"""SET self-test for all NTCIP 1202 read-write objects (in-process)."""
from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

_AGENT_ROOT = Path(__file__).resolve().parent.parent
_TEST_AGENT = _AGENT_ROOT.parent
REPORT_DIR = _TEST_AGENT / "reports"
REPORT_MD = REPORT_DIR / "1202-set-selftest-report.md"
REPORT_CSV = REPORT_DIR / "1202-set-selftest-report.csv"
DOCS_SET_MD = _TEST_AGENT / "docs" / "1202DEFAULT_DATA-OIDs-SET.md"

sys.path.insert(0, str(_AGENT_ROOT))

from instrum import FlatMibInstrum  # noqa: E402
from mib_loader import MibLoader  # noqa: E402
from oid_utils import DEVICES_OID_ROOT  # noqa: E402
from sim_data.set_test_runner import (  # noqa: E402
    SetTestResult,
    run_index_not_accessible_reject,
    run_readonly_reject,
    run_writable_set_readback,
)
from sim_data.set_values import collect_readonly_negative_samples, collect_writable_set_cases  # noqa: E402

DEV_CAP = 8
MIB_FILE = "1202v0218.mib"

# INDEX columns (not-accessible) — must reject Set
INDEX_REJECT_OIDS = [
    (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 1, 1),  # phaseNumber.1
    (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 8, 2, 1, 1, 1),  # channelNumber.1
    (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 4, 9, 1, 1, 1, 1),  # splitNumber.1.1 (dual index)
]

DUAL_INDEX_SPOT = [
    "splitTime",
    "sequenceData",
    "dayPlanHour",
    "auxIOPortValue",
    "auxIOPortDescription",
]


def run_selftest() -> tuple[list[SetTestResult], dict]:
    loader = MibLoader(_TEST_AGENT / "mibs" / "mibs_old", dev_cap=DEV_CAP, oid_root=DEVICES_OID_ROOT)
    vals = loader.load()
    instrum = FlatMibInstrum(
        vals,
        registry=loader.oid_registry,
        write_communities={"public"},
    )

    writable = collect_writable_set_cases(loader.oid_registry)
    readonly = collect_readonly_negative_samples(loader.oid_registry, limit=20)

    results: list[SetTestResult] = []
    results.extend(run_writable_set_readback(instrum, writable))
    results.extend(run_readonly_reject(instrum, readonly))
    results.extend(run_index_not_accessible_reject(instrum, INDEX_REJECT_OIDS))

    dual_pass = {n: False for n in DUAL_INDEX_SPOT}
    for r in results:
        if r.name in dual_pass and r.status == "PASS" and r.phase == "set-readback":
            dual_pass[r.name] = True

    meta = {
        "dev_cap": DEV_CAP,
        "writable_cases": len(writable),
        "readonly_cases": len(readonly),
        "index_reject_cases": len(INDEX_REJECT_OIDS),
        "dual_index_spot": dual_pass,
        "instances": len(vals),
    }
    return results, meta


def write_report(results: list[SetTestResult], meta: dict) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1
    status = "PASS" if counts["FAIL"] == 0 else "FAIL"

    lines = [
        "# NTCIP 1202 SET 自测报告",
        "",
        "> **版本标注 SET** — 与 Get/默认值报告 `1202-selftest-report.md` 区分",
        "",
        f"- **时间**: {ts}",
        f"- **MIB**: `mibs/mibs_old/{MIB_FILE}`",
        f"- **OID 范围**: `1.3.6.1.4.1.1206.4.2.1` (asc)",
        f"- **dev_cap**: {meta['dev_cap']}",
        f"- **持久化策略**: 方案 A（进程内 Set 读回；重启恢复默认）",
        f"- **结果**: **{status}**",
        "",
        "## 1. 汇总",
        "",
        "| 指标 | 值 |",
        "|---|---|",
        f"| 可写对象 Set 读回 | {meta['writable_cases']} |",
        f"| 只读拒绝抽样 | {meta['readonly_cases']} |",
        f"| INDEX 拒绝 | {meta['index_reject_cases']} |",
        f"| ASC 实例 OID 总数 | {meta['instances']} |",
        f"| PASS | {counts['PASS']} |",
        f"| FAIL | {counts['FAIL']} |",
        f"| SKIP | {counts['SKIP']} |",
        "",
        "## 2. 双索引表 Spot（5 张）",
        "",
        "| 对象 | Set 读回 |",
        "|---|---|",
    ]
    for name, ok in meta["dual_index_spot"].items():
        lines.append(f"| `{name}` | {'PASS' if ok else 'FAIL'} |")

    lines.extend(
        [
            "",
            "## 3. 可写对象 Set 明细",
            "",
            "| # | 对象名 | 实例 OID | old | new | 结果 | 说明 |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    n = 0
    for r in results:
        if r.phase != "set-readback":
            continue
        n += 1
        lines.append(
            f"| {n} | `{r.name}` | `{r.instance_oid}` | {r.old_value[:30]} | {r.new_value[:30]} | {r.status} | {r.detail} |"
        )

    fails = [r for r in results if r.status == "FAIL"]
    if fails:
        lines.extend(["", "## 4. 失败项", ""])
        for r in fails:
            lines.append(f"- **{r.phase}** `{r.name}` `{r.instance_oid}`: {r.detail}")

    lines.extend(
        [
            "",
            "## 5. 复现命令",
            "",
            "```bash",
            "cd test-agent/snmp-agent",
            "py scripts/selftest_1202_set.py",
            "py scripts/snmp_set_test.py --port 1161",
            "py -m pytest tests/ -q",
            "```",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    with REPORT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "phase",
                "name",
                "instance_oid",
                "access",
                "syntax",
                "status",
                "detail",
                "old_value",
                "new_value",
            ],
        )
        w.writeheader()
        for r in results:
            w.writerow(
                {
                    "phase": r.phase,
                    "name": r.name,
                    "instance_oid": r.instance_oid,
                    "access": r.access,
                    "syntax": r.syntax,
                    "status": r.status,
                    "detail": r.detail,
                    "old_value": r.old_value,
                    "new_value": r.new_value,
                }
            )

    _write_docs_set_index(results, meta, ts, status)


def _write_docs_set_index(results: list[SetTestResult], meta: dict, ts: str, status: str) -> None:
    """Generate docs/1202DEFAULT_DATA-OIDs-SET.md — SET version of OID listing."""
    by_name = {r.name: r for r in results if r.phase == "set-readback"}
    DOCS_SET_MD.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# 1202 全部对象清单（SET 版）",
        "",
        "> **版本标注 SET** — 在 `1202DEFAULT_DATA-OIDs.md`（Get/默认值）基础上增加 Set 测试结果",
        "",
        f"| 项 | 值 |",
        f"|---|---|",
        f"| 生成时间 | {ts} |",
        f"| SET 自测 | **{status}** |",
        f"| dev_cap | {meta['dev_cap']} |",
        f"| 可写对象数 | {meta['writable_cases']} |",
        "",
        "## Set 测试说明",
        "",
        "- **read-write**：进程内 Set → Get 读回 + 非法值拒绝",
        "- **read-only / not-accessible**：Set 拒绝",
        "- 重启 Agent 后恢复默认（方案 A，不做持久化）",
        "",
        "## 可写对象 Set 结果",
        "",
        "| # | 对象名 | 实例 OID | Set 读回 | 说明 |",
        "|---|---|---|---|---|",
    ]
    for i, (name, r) in enumerate(sorted(by_name.items()), 1):
        lines.append(f"| {i} | `{name}` | `{r.instance_oid}` | {r.status} | {r.detail} |")

    lines.extend(
        [
            "",
            "完整默认值见 [1202DEFAULT_DATA-OIDs.md](1202DEFAULT_DATA-OIDs.md)。",
            "",
            "重新生成：",
            "",
            "```bash",
            "py scripts/selftest_1202_set.py",
            "```",
        ]
    )
    DOCS_SET_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    results, meta = run_selftest()
    write_report(results, meta)
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    for r in results:
        counts[r.status] += 1
    print(f"Report: {REPORT_MD}")
    print(f"CSV:    {REPORT_CSV}")
    print(f"Docs:   {DOCS_SET_MD}")
    print(f"Status: {'PASS' if counts['FAIL'] == 0 else 'FAIL'}")
    print(f"PASS={counts['PASS']} FAIL={counts['FAIL']} SKIP={counts['SKIP']}")
    print(f"Writable: {meta['writable_cases']}, readonly reject: {meta['readonly_cases']}")
    return 0 if counts["FAIL"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
