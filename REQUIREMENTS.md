# NTCIP SNMP Agent 项目需求任务书（v2）

## 1. 项目概述

| 项 | 说明 |
|---|---|
| **项目名称** | test-agent SNMP Agent（NTCIP 字段设备模拟 Agent） |
| **工程目录** | `test-agent/snmp-agent/`（**独立项目**） |
| **MIB 来源** | `test-agent/mibs/mibs_old/`（唯一 MIB 输入） |
| **核心目标** | MIB Browser 对 NTCIP OID 树 Get / Walk / Set 时，**完整返回**可访问对象数据 |
| **数据策略** | **全部模拟填充**；表/列表按 MIB 允许**最大行数**展开 |
| **附加能力** | 支持 **SNMP Trap** 发送 |

## 2. 项目定位与原则

### 2.1 定位

1. NTCIP MIB 的**可查询假设备**，供 MIB Browser 完整 Walk / Get 测试
2. Trap 源，供管理站 / Trap 工具验证接收链路
3. **不**承担真实 ASC 业务逻辑，不替代 NTCIP Exerciser

### 2.2 数据填充原则

| 原则 | 说明 |
|---|---|
| P1 全量模拟 | 所有可访问 OID 均有预置模拟值 |
| P2 表满填 | TABLE 按 `max*` 或 INDEX SYNTAX 上限满行展开 |
| P3 语义一致 | `maxPhases` 与 `phaseTable` 行数等关联字段一致 |
| P4 类型合法 | 值落在 SYNTAX 范围内 |
| P5 可追溯 | 默认值来自 `docs/1201DEFAULT_DATA.md` / `docs/1202DEFAULT_DATA.md` / `default_data.yaml` 或 `# SIM-DATA` 注释 |

### 2.3 默认数据管理

- **推荐**：`default_data.yaml` + `docs/1201DEFAULT_DATA.md` + `docs/1202DEFAULT_DATA.md`
- **允许**：`sim_data/default_values.py` 写死，须 `# SIM-DATA:` 注释

## 3. MIB 资产

```
test-agent/mibs/mibs_old/
├── 8004v0134.mib   → NTCIP8004-A-2004
├── 1103v0125.mib   → NTCIP1103-A-2004
├── 1201v0227.mib   → NTCIP1201-2004
└── 1202v0218.mib   → NTCIP1202-2004
```

加载顺序：`RFC1155-SMI → RFC-1212 → RFC1213-MIB → 8004 → {1103,1201} → 1202`

OID 根：`1.3.6.1.4.1.1206`

## 4. 功能需求摘要

### FR-01 MIB 解析
- 解析 OBJECT-TYPE、Table、INDEX、SYNTAX、ACCESS
- 识别 `max*` scalar 作为表行数依据

### FR-02 模拟数据填充
- 所有 scalar（ACCESS ≠ not-accessible）有模拟值，实例后缀 `.0`
- 表按 max 满填；双索引表按各维上限笛卡尔展开
- 支持 `default_data.yaml` 覆盖
- 可选 `--dev-cap N`（仅开发，非验收）

### FR-03 文档
- 必交付 `docs/1201DEFAULT_DATA.md`、`docs/1202DEFAULT_DATA.md`（及索引 `docs/DEFAULT_DATA.md`）
- 可选 `default_data.yaml`

### FR-04 SNMP Agent
- UDP v1/v2c：Get / GetNext / GetBulk / Set
- MIB Browser 对 `1.3.6.1.4.1.1206` 可完整 Walk

### FR-05 SNMP Trap
- v1 / v2c Trap 发送至 `--trap-host:--trap-port`
- 支持 coldStart、warmStart、enterprise-specific
- CLI 触发：`--send-trap TYPE` 或 `scripts/trap_send.py`

## 5. 工程结构

```
test-agent/
├── README.md
├── REQUIREMENTS.md
├── docs/
│   ├── STRUCTURE.md          目录与文件说明
│   ├── DEFAULT_DATA.md       模拟数据索引
│   ├── 1201DEFAULT_DATA.md
│   └── 1202DEFAULT_DATA.md
├── mibs/mibs_old/
├── tree/
├── reports/
└── snmp-agent/
    ├── agent.py
    ├── mib_loader.py / smi_parser.py / table_expander.py
    ├── value_factory.py / instrum.py / oid_registry.py
    ├── trap_sender.py
    ├── sim_data/
    ├── scripts/              trap_send.py, selftest_1202.py
    ├── tests/
    ├── default_data.yaml
    ├── deps/
    ├── requirements.txt
    └── README.md
```

## 6. 验收标准

### P0
- [ ] 四 MIB 加载成功
- [ ] 满填 Walk 无大段 noSuchObject
- [ ] `docs/1201DEFAULT_DATA.md` / `docs/1202DEFAULT_DATA.md` 与代码可对照
- [ ] Trap v1 coldStart 与 v2c enterprise Trap 可接收

### P1
- [ ] Set 读回
- [ ] 双索引表 index 列正确

## 7. 交付物

| # | 交付物 |
|---|---|
| D1 | `snmp-agent/` 源码 |
| D2 | `requirements.txt` |
| D3 | `README.md` |
| D4 | **`docs/1201DEFAULT_DATA.md`**、**`docs/1202DEFAULT_DATA.md`**、`docs/DEFAULT_DATA.md` |
| D5 | `default_data.yaml` |
| D6 | 测试 / Walk 记录 |
| D7 | Trap 联调记录 |

## 8. 风险

| 风险 | 对策 |
|---|---|
| 满填内存/启动慢 | README 说明；`--dev-cap` 开发用 |
| MIB 无 TRAP-TYPE | 标准 Trap + enterprise OID |
| 双索引 max 歧义 | INDEX SYNTAX 优先 + 映射表 |

---

*文档版本：v2 | 日期：2026-07-03*
