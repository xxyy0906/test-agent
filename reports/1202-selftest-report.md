# NTCIP 1202 自测报告

- **时间**: 2026-07-07 02:52 UTC
- **MIB**: `mibs/mibs_old/1202v0218.mib`
- **OID 范围**: `1.3.6.1.4.1.1206.4.2.1` (asc)
- **dev_cap**: 3
- **结果**: **PASS**

## 1. 汇总

| 指标 | 值 |
|---|---|
| 1202 定义对象数 | 253 |
| 校验单元格数 | 197 |
| ASC 实例 OID 总数 | 543 |
| 缺失 | 0 |
| 类型/范围错误 | 0 |
| 错误 table-column scalar (.0) | 0 |
| 抽样失败 | 0 |
| Get 失败 | 0 |

## 2. 默认值规则

| 类型 | 规则 |
|---|---|
| INTEGER (lo..hi) | 取 hi；INDEX 列取行号 |
| INTEGER { enum } | 取最大 enum 值 |
| DEFVAL | 优先使用 MIB DEFVAL |
| Counter / Gauge | Counter32 / Gauge32 |
| OCTET STRING | DEFVAL `""` → 空串；否则按 SIZE |

## 3. 表展开 (dev_cap=3)

| 表名 | 行数 | 可访问列数 |
|---|---|---|
| `alarmGroupTable` | 3 | 2 |
| `channelStatusGroupTable` | 3 | 4 |
| `channelTable` | 3 | 5 |
| `overlapStatusGroupTable` | 3 | 4 |
| `overlapTable` | 3 | 7 |
| `patternTable` | 3 | 5 |
| `pedestrianDetectorTable` | 3 | 6 |
| `phaseControlGroupTable` | 3 | 7 |
| `phaseStatusGroupTable` | 3 | 11 |
| `phaseTable` | 3 | 23 |
| `port1Table` | 3 | 5 |
| `preemptControlTable` | 3 | 2 |
| `preemptTable` | 3 | 25 |
| `ringControlGroupTable` | 3 | 8 |
| `ringStatusTable` | 3 | 1 |
| `sequenceTable` | 9 | 3 |
| `specialFunctionOutputTable` | 3 | 3 |
| `splitTable` | 9 | 5 |
| `timebaseAscActionTable` | 3 | 4 |
| `vehicleDetectorStatusGroupTable` | 3 | 3 |
| `vehicleDetectorTable` | 3 | 14 |
| `volumeOccupancyTable` | 3 | 2 |

## 4. 抽样 OID 验证

| 对象 | OID | 期望值 |
|---|---|---|
| maxPhases | `1.3.6.1.4.1.1206.4.2.1.1.1.0` | 255 |
| phaseNumber.1 | `1.3.6.1.4.1.1206.4.2.1.1.2.1.1.1` | 1 |
| phasePedestrianClear.1 | `1.3.6.1.4.1.1206.4.2.1.1.2.1.3.1` | 255 |
| phaseRedClear.1 (col 1.9) | `1.3.6.1.4.1.1206.4.2.1.1.2.1.9.1` | 255 |
| phaseRedRevert.1 (col 1.10) | `1.3.6.1.4.1.1206.4.2.1.1.2.1.10.1` | 255 |
| preemptControl.1 DEFVAL 0 | `1.3.6.1.4.1.1206.4.2.1.6.2.1.2.1` | 0 |
| preemptMinimumGreen.1 DEFVAL 255 | `1.3.6.1.4.1.1206.4.2.1.6.2.1.6.1` | 255 |
| preemptDwellGreen.1 DEFVAL 10 | `1.3.6.1.4.1.1206.4.2.1.6.2.1.10.1` | 10 |
| preemptTrackPhase.1 DEFVAL empty | `1.3.6.1.4.1.1206.4.2.1.6.2.1.12.1` |  |
| splitMode enum max | `1.3.6.1.4.1.1206.4.2.1.4.1.0` | (enum max) |

## 8. phaseTable 列 OID 对照

| 列后缀 | 对象名 |
|---|---|
| 1.9 | phaseRedClear |
| 1.10 | **phaseRedRevert** |

完整实例 = 表 OID + 列后缀 + 行号，例如 phaseRedRevert 第1行：`…1.1.2.1.10.1`

## 9. 复现命令

```bash
cd test-agent/snmp-agent
py scripts/selftest_1202.py
py -m pytest tests/ -q
```