# 1201DEFAULT_DATA.md — NTCIP 1201 Global 模拟数据说明

**OID 范围：`1.3.6.1.4.1.1206.4.2.6`（devices.6 = global）**

| 项 | 值 |
|---|---|
| MIB 源文件 | `mibs/mibs_old/1201v0227.mib` |
| 实现代码 | `snmp-agent/sim_data/ntcip1201.py` + `resolver.py` |
| 关联 MIB | 1103（globalReport / security 节点，见 §5） |
| OID 树参考 | `test-agent/tree/1201v0227-tree.md` |

## 1. 填充规则

| 类型 | 规则 |
|---|---|
| INTEGER (lo..hi) | 非 INDEX 列取 **hi** |
| INTEGER { enum } | 有 DEFVAL 用 DEFVAL；否则取 **最大 enum 值** |
| Counter | 有 DEFVAL `{0}` 用 **0**（globalTime）；否则 Counter32 上限 |
| Gauge | Gauge32 类型上限 |
| OCTET STRING / DisplayString / OwnerString | 语义化 ASCII（见下表）；无定义时按 SIZE 上限 |
| OBJECT IDENTIFIER | 指向 ASC `1.3.6.1.4.1.1206.4.2.1` 或 action OID |
| INDEX 列 | **行号**（1..max），不用范围上限 |
| Scalar 实例 | SNMP 实例 OID = 定义 OID + `.0` |

## 2. Scalar 清单

### globalConfiguration

| 对象 | SYNTAX | 模拟值 |
|---|---|---|
| globalSetIDParameter | INTEGER (0..65535) | 65535 |
| globalMaxModules | INTEGER (1..255) | 255 |
| controllerBaseStandards | OCTET STRING (0..256) | `NTCIP 1201:v02.27\r\nNTCIP 1202:v02.18\r\nNTCIP 1103:v01.25` |

### globalDBManagement

| 对象 | SYNTAX | 模拟值 |
|---|---|---|
| dbCreateTransaction | ENUM, DEFVAL normal | 1 |
| dbVerifyStatus | ENUM | 3 (doneWithNoError) |
| dbVerifyError | OCTET STRING (0..255) | 空串 |

### globalTimeManagement

| 对象 | SYNTAX | 模拟值 |
|---|---|---|
| globalTime | Counter, DEFVAL 0 | 0 |
| globalDaylightSaving | ENUM, DEFVAL disableDST | 2 |
| maxTimeBaseScheduleEntries | INTEGER (1..65535) | 65535 |
| timeBaseScheduleTable-status | INTEGER (0..65535) | 1 |
| maxDayPlans / maxDayPlanEvents | INTEGER (1..255) | 255 |
| dayPlanStatus | INTEGER (0..255) | 1 |
| controllerStandardTimeZone | INTEGER (-43200..43200) | 43200 |
| controllerLocalTime | Counter | 0 |

### profilesPMPP / auxIO

| 对象 | SYNTAX | 模拟值 |
|---|---|---|
| maxGroupAddresses | INTEGER (1..255) | 255 |
| auxIOTableNumDigitalPorts | INTEGER (1..255) | 255 |
| auxIOTableNumAnalogPorts | INTEGER (1..255) | 255 |

## 3. 表行模板

| 表 | 行数来源 | 说明 |
|---|---|---|
| globalModuleTable | globalMaxModules (255) | 见 §3.1 |
| timeBaseScheduleTable | maxTimeBaseScheduleEntries | 见 §3.2 |
| timeBaseDayPlanTable | maxDayPlans × maxDayPlanEvents | 见 §3.3 |
| hdlcGroupAddressTable | maxGroupAddresses | 见 §3.4 |
| auxIOTable | auxIOTableNumDigitalPorts × auxIOTableNumAnalogPorts | 见 §3.5 |

### 3.1 globalModuleTable（行 i）

| 列 | 值 |
|---|---|
| moduleNumber | i |
| moduleDeviceNode | 1.3.6.1.4.1.1206.4.2.1 |
| moduleMake | `SIM` |
| moduleModel | `NTCIP1201-AGENT` |
| moduleVersion | `20260706 - v1.0.0` |
| moduleType | 3 (software) |

### 3.2 timeBaseScheduleTable（行 i）

| 列 | 值 |
|---|---|
| timeBaseScheduleNumber | i |
| timeBaseScheduleMonth | 65535 |
| timeBaseScheduleDay | 255 |
| timeBaseScheduleDate | 4294967295 |
| timeBaseScheduleDayPlan | min(i, 255) |

### 3.3 timeBaseDayPlanTable（plan i, event j）

| 列 | 值 |
|---|---|
| dayPlanNumber | i |
| dayPlanEventNumber | j |
| dayPlanHour | 23 |
| dayPlanMinute | 59 |
| dayPlanActionNumberOID | 1.3.6.1.4.1.1206.4.2.1.5.2.1.1.0 |

### 3.4 hdlcGroupAddressTable（行 i）

| 列 | 值 |
|---|---|
| hdlcGroupAddressIndex | i |
| hdlcGroupAddressNumber | 0（DEFVAL，禁用行） |

### 3.5 auxIOTable（type × port）

| 列 | 规则 |
|---|---|
| auxIOPortType | 2=Analog, 3=Digital |
| auxIOPortNumber | 端口号 |
| auxIOPortDescription | `Analog Port N` / `Digital Port N` |
| auxIOPortResolution | 32（INTEGER 上限） |
| auxIOPortValue | 4294967295 |
| auxIOPortDirection | analog=output(1), digital=input(2) |
| auxIOPortLastCommandedState | 0 |

## 4. YAML 覆盖

编辑 `snmp-agent/default_data.yaml`（1201 标量示例）：

```yaml
scalars:
  globalMaxModules: 8
  maxDayPlans: 16
oids:
  "1.3.6.1.4.1.1206.4.2.6.1.2.0": 255
```

## 5. NTCIP1103（global 下节点）

> 实现：`snmp-agent/sim_data/ntcip1103.py`

| 对象 | 模拟值规则 |
|---|---|
| maxEventClasses | 255 → eventClassTable 255 行 |
| maxEventLogConfigs | 65535 → eventLogConfigTable 满填 |
| maxEventLogSize | 65535；eventLogTable 第二维 eventLogNumber (1..255) |
| communityNamesMax | 255 → communityNameTable 255 行 |
| communityNameTable.communityNameUser | 行 1=`public`，行 2=`administrator` |
| communityNameAccessMask | Gauge DEFVAL 4294967295 |

> logicalNameTranslation、dynObj 等在 application 子树，不在 `...4.2.6`；需 `--all-ntcip`。

## 6. 相关文档

- [1202DEFAULT_DATA.md](1202DEFAULT_DATA.md) — ASC (1202) 默认值
- [STRUCTURE.md](STRUCTURE.md) — 项目目录说明
