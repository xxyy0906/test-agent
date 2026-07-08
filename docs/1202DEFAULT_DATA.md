# 1202DEFAULT_DATA.md — NTCIP 1202 ASC 模拟数据说明

**OID 范围：`1.3.6.1.4.1.1206.4.2.1`（devices.1 = asc）**

| 项 | 值 |
|---|---|
| MIB 源文件 | `mibs/mibs_old/1202v0218.mib` |
| 实现代码 | `snmp-agent/sim_data/ntcip1202.py` + `resolver.py` |
| OID 树参考 | `tree/1202v0218-tree.md` |
| **完整 OID 清单** | [1202DEFAULT_DATA-OIDs.md](1202DEFAULT_DATA-OIDs.md)（253 对象） |
| 自测报告 | `test-agent/reports/1202-selftest-report.md` |

## 1. 填充规则

| 类型 | 规则 |
|---|---|
| INTEGER (lo..hi) | 非 INDEX 列取 **hi**；有 DEFVAL 时优先 DEFVAL |
| INTEGER { enum } | 取 **最大 enum 值** |
| INDEX 列 | **行号**（1..max*） |
| Counter / Gauge | Counter32 / Gauge32 类型上限 |
| OCTET STRING / OwnerString | DEFVAL `{ "" }` → 空串；否则按 SIZE 填充 |
| OBJECT IDENTIFIER | 指向 `1.3.6.1.4.1.1206.4.2.1`（ASC 根） |
| Scalar 实例 | SNMP 实例 OID = 定义 OID + `.0` |

> 通用解析逻辑见 `snmp-agent/sim_data/resolver.py`；1202 特化见 `ntcip1202.py`。

## 2. ASC 分支概览

```
1.3.6.1.4.1.1206.4.2.1  asc
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
```

## 3. max* Scalar（表行数依据）

| 对象 | SYNTAX 范围 | 默认值 | 控制表 |
|---|---|---|---|
| maxPhases | 2..255 | 255 | phaseTable |
| maxPhaseGroups | 1..255 | 255 | phaseStatusGroupTable, phaseControlGroupTable |
| maxVehicleDetectors | 1..255 | 255 | vehicleDetectorTable, volumeOccupancyTable |
| maxVehicleDetectorStatusGroups | 1..255 | 255 | vehicleDetectorStatusGroupTable |
| maxPedestrianDetectors | 1..255 | 255 | pedestrianDetectorTable |
| maxAlarmGroups | 1..255 | 255 | alarmGroupTable |
| maxSpecialFunctionOutputs | 1..255 | 255 | specialFunctionOutputTable |
| maxPatterns | 1..253 | 253 | patternTable |
| maxSplits | 1..255 | 255 | splitTable（双索引：split × phase） |
| maxTimebaseAscActions | 1..255 | 255 | timebaseAscActionTable |
| maxPreempts | 1..255 | 255 | preemptTable, preemptControlTable |
| maxRings | 1..255 | 255 | sequenceTable, ringStatusTable |
| maxSequences | 1..255 | 255 | sequenceTable（双索引：ring × sequence） |
| maxRingControlGroups | 1..255 | 255 | ringControlGroupTable |
| maxChannels | 1..255 | 255 | channelTable |
| maxChannelStatusGroups | 1..255 | 255 | channelStatusGroupTable |
| maxOverlaps | 1..255 | 255 | overlapTable |
| maxOverlapStatusGroups | 1..255 | 255 | overlapStatusGroupTable |
| maxPort1Addresses | 1..255 | 255 | port1Table |

## 4. 表与行数

| 表 | 行数 / 维度 |
|---|---|
| phaseTable | maxPhases |
| phaseStatusGroupTable / phaseControlGroupTable | maxPhaseGroups |
| vehicleDetectorTable | maxVehicleDetectors |
| vehicleDetectorStatusGroupTable | maxVehicleDetectorStatusGroups |
| volumeOccupancyTable | maxVehicleDetectors |
| pedestrianDetectorTable | maxPedestrianDetectors |
| alarmGroupTable | maxAlarmGroups |
| specialFunctionOutputTable | maxSpecialFunctionOutputs |
| patternTable | maxPatterns |
| splitTable | maxSplits × maxPhases |
| timebaseAscActionTable | maxTimebaseAscActions |
| preemptTable / preemptControlTable | maxPreempts |
| sequenceTable | maxSequences × maxRings |
| ringControlGroupTable | maxRingControlGroups |
| ringStatusTable | maxRings |
| channelTable | maxChannels |
| channelStatusGroupTable | maxChannelStatusGroups |
| overlapTable | maxOverlaps |
| overlapStatusGroupTable | maxOverlapStatusGroups |
| port1Table | maxPort1Addresses |

## 5. 特化行模板（ntcip1202.py）

仅 INDEX 列或 DEFVAL 列在代码中显式指定；其余列由 resolver 按 SYNTAX/DEFVAL 生成。

| 表 | 列 | 值 |
|---|---|---|
| phaseTable | phaseNumber | 行号 i |
| vehicleDetectorTable | vehicleDetectorNumber | 行号 i |
| pedestrianDetectorTable | pedestrianDetectorNumber | 行号 i |
| preemptTable | preemptNumber | 行号 i |
| port1Table | port1AddressIndex | 行号 i |
| port1Table | port1Address / port1DeviceType / port1Description | 空串（DEFVAL） |

## 6. preemptTable DEFVAL 示例

| 列 | 默认值 | 说明 |
|---|---|---|
| preemptControl | 0 | DEFVAL |
| preemptLink | 0 | DEFVAL |
| preemptDelay | 0 | DEFVAL |
| preemptMinimumDuration | 0 | DEFVAL |
| preemptMinimumGreen | 255 | DEFVAL |
| preemptDwellGreen | 10 | DEFVAL |
| preemptTrackPhase | 空 OCTET STRING | DEFVAL `{ "" }` |
| preemptAdvanceWarning | 0 | DEFVAL |
| preemptCallPhase | 空 OCTET STRING | DEFVAL |

## 7. coord / unit / ascBlock Scalar 示例

### coord（读多写少，多数取 enum 最大或 INTEGER 上限）

| 对象 | 典型值 |
|---|---|
| coordOperationalMode | enum 最大值 |
| coordCorrectionMode | enum 最大值 |
| coordMaximumMode | enum 最大值 |
| coordForceMode | enum 最大值 |
| patternTableType | 4 (offset5) |
| coordPatternStatus / coordCycleStatus / coordSyncStatus | INTEGER 上限 |

### unit

| 对象 | 典型值 |
|---|---|
| unitStartUpFlash / unitAutoPedestrianClear / unitBackupTime 等 | INTEGER (0..255) → 255 |
| unitControl | read-write，INTEGER 上限 |
| unitControlStatus / unitFlashStatus / unitAlarmStatus* | read-only，enum 最大或 INTEGER 上限 |

### ascBlock

| 对象 | 典型值 |
|---|---|
| ascBlockGetControl | 空 OCTET STRING（SIZE 2..12，lo=0 填充） |
| ascBlockData | 空 OCTET STRING（SIZE 2..484） |
| ascBlockErrorStatus | 65535 |

## 8. phaseTable 列默认值（典型）

| 列 | OID 后缀 | 默认值 |
|---|---|---|
| phaseNumber | 1.1 | 行号（INDEX） |
| phaseWalk | 1.2 | 255 |
| phasePedestrianClear | 1.3 | 255 |
| phaseMinimumGreen | 1.4 | 255 |
| phaseYellowChange | 1.8 | 255 |
| phaseRedClear | 1.9 | 255 |
| phaseRedRevert | 1.10 | 255 |
| phaseStartup | 1.20 | 6（enum 最大：redClear） |
| phaseOptions | 1.21 | 65535 |

> phaseRedClear = 后缀 **1.9**；phaseRedRevert = 后缀 **1.10**。  
> 实例示例：phaseRedRevert 第 1 行 = `…1.1.2.1.10.1` = 255

## 9. splitTable / splitMode

双索引表：`splitNumber` × `splitPhase`。

| 列 | 规则 |
|---|---|
| splitNumber / splitPhase | INDEX，取行号 |
| splitTime | 255 |
| splitMode | 7（enum 最大：phaseOmitted） |
| splitCoordPhase | 1 |

标量 `splitMode`（coord 下）为独立对象，enum 取最大值。

## 10. YAML 覆盖

```yaml
scalars:
  maxPhases: 8
  maxPatterns: 16
oids:
  "1.3.6.1.4.1.1206.4.2.1.1.1.0": 42
  "1.3.6.1.4.1.1206.4.2.1.1.2.1.3.1": 100
```

## 11. 开发与验收

```bash
cd test-agent/snmp-agent
py agent.py --port 1161 --dev-cap 8
py scripts/selftest_1202.py
```

`--dev-cap N` 仅用于开发加速，**正式 Walk 验收应满填**（不带 `--dev-cap`）。

## 12. 相关文档

- [1202DEFAULT_DATA-OIDs.md](1202DEFAULT_DATA-OIDs.md) — **253 对象逐条 OID + 默认值**
- [1201DEFAULT_DATA.md](1201DEFAULT_DATA.md) — Global (1201) 默认值
- [STRUCTURE.md](STRUCTURE.md) — 项目目录说明

重新生成 OID 清单：

```bash
cd test-agent/snmp-agent
py scripts/gen_1202_defaults.py
```
