# 项目目录结构说明

本文档说明 `test-agent/` 下每个目录与文件的用途。

```
test-agent/
├── README.md                 项目入口、快速开始
├── REQUIREMENTS.md           需求任务书（验收标准）
├── .gitignore
├── docs/                     文档（本目录）
├── mibs/mibs_old/            MIB 源文件（只读输入）
├── tree/                     OID 树生成与导出
├── reports/                  自测报告（生成物）
└── snmp-agent/               SNMP Agent 源码与测试
```

---

## docs/ — 文档

| 文件 | 用途 |
|---|---|
| `README.md` | 文档索引 |
| `STRUCTURE.md` | **本文件**：目录/文件说明 |
| `UBUNTU.md` | Ubuntu 安装依赖、venv、启动与防火墙 |
| `DEFAULT_DATA.md` | 模拟数据总索引、Trap VarBind、YAML 覆盖 |
| `1201DEFAULT_DATA.md` | Global (1201 + 1103) 默认值规范 |
| `1202DEFAULT_DATA-OIDs.md` | 1202 全部对象默认值清单（Get 版） |
| `1202DEFAULT_DATA-OIDs-SET.md` | **SET 版**：可写对象 Set 读回测试结果 |
| `1202DEFAULT_DATA.md` | ASC (1202) 默认值规范 |

---

## mibs/mibs_old/ — MIB 输入

Agent **唯一** MIB 来源，加载顺序见 `snmp-agent/mib_loader.py`。

| 文件 | MIB |
|---|---|
| `8004v0134.mib` | NTCIP8004 设备树 |
| `1103v0125.mib` | NTCIP1103（report/security） |
| `1201v0227.mib` | NTCIP1201 Global |
| `1202v0218.mib` | NTCIP1202 ASC |

---

## tree/ — OID 树工具

从 MIB 生成可读 OID 树，用于核对类型/范围/ACCESS。

| 文件 | 用途 |
|---|---|
| `gen_mib_tree.py` | **主生成器**（`py gen_mib_tree.py 1202v0218.mib`） |
| `gen_1201_tree.py` | 1201 快捷入口（调用 gen_mib_tree） |
| `gen_1202_tree.py` | 1202 快捷入口 |
| `1201v0227-tree.md` / `.txt` / `-flat.csv` | 1201 导出（59 对象） |
| `1202v0218-tree.md` / `.txt` / `-flat.csv` | 1202 导出（253 对象） |
| `README.md` | tree 目录说明 |

重新生成：

```bash
cd test-agent/tree
py gen_mib_tree.py 1201v0227.mib
py gen_mib_tree.py 1202v0218.mib
```

---

## reports/ — 自测报告

| 文件 | 用途 |
|---|---|
| `1202-selftest-report.md` | 1202 Get/默认值自测（原版） |
| `1202-set-selftest-report.md` | **SET 版**：137 可写对象 Set 读回 + 拒绝测试 |
| `1202-set-selftest-report.csv` | SET 自测明细 CSV |

---

## snmp-agent/ — Agent 工程

### 入口与 CLI

| 文件 | 用途 |
|---|---|
| `agent.py` | **主程序**：启动 UDP SNMP Agent |
| `scripts/trap_send.py` | 独立 CLI：发送 Trap/Inform |
| `scripts/selftest_1202.py` | 1202 Get/默认值自测 + 写报告 |
| `scripts/selftest_1202_set.py` | **SET 版**：1202 可写对象 Set 全量自测 |
| `scripts/snmp_get_test.py` | UDP Get 冒烟 |
| `scripts/snmp_set_test.py` | **SET 版**：UDP Set 冒烟/全量 |

### 核心模块（根目录）

| 文件 | 用途 |
|---|---|
| `mib_loader.py` | 加载 MIB、展开表、构建 OID→值 字典 |
| `smi_parser.py` | SMI 解析（OBJECT-TYPE、TABLE、INDEX、SYNTAX） |
| `table_expander.py` | 按 max* 满行展开表 |
| `value_factory.py` | 按 SYNTAX 生成类型上限默认值 |
| `instrum.py` | SNMP Get/GetNext/GetBulk/Set 实现 |
| `oid_registry.py` | OID 元数据（ACCESS/SYNTAX），供 Set 校验 |
| `oid_utils.py` | OID 前缀工具（devices/asc/global） |
| `trap_sender.py` | Trap/Inform 发送库（v1/v2c/v3） |

### sim_data/ — 模拟数据

| 文件 | 用途 |
|---|---|
| `resolver.py` | **总解析器**：SYNTAX + DEFVAL + 模块规则 |
| `mib_syntax.py` | 从 MIB 文件加载完整 SYNTAX 文本 |
| `validate.py` | 校验值是否在 SYNTAX 范围内 |
| `loader.py` | 读取 `default_data.yaml` 覆盖 |
| `ntcip1201.py` | 1201 Global 特化标量/表行 |
| `ntcip1202.py` | 1202 ASC 特化表行 |
| `ntcip1103.py` | 1103 communityName 等 |
| `default_values.py` | 常量（enterprise OID、community 名） |

### tests/ — 单元测试

| 文件 | 用途 |
|---|---|
| `test_mib_loader.py` | MIB 加载与 devices 覆盖 |
| `test_mib_coverage.py` | 1201/1202 对象覆盖率 |
| `test_ntcip1201.py` | 1201 全对象默认值 |
| `test_instrum.py` | Get 解析（标量/表列/双击兼容） |
| `test_snmp_ops.py` | Get/Set/GetNext 操作 |

运行：`cd snmp-agent && py -m pytest tests/ -q`

### deps/ — RFC 依赖 MIB

| 文件 | 用途 |
|---|---|
| `Rfc1155.smi` / `rfc1212.smi` / `rfc1158.smi` | SMI 基础 |
| `RFC1213-MIB.mib` | MIB-II（解析依赖，Agent 不填充） |

### 配置与说明

| 文件 | 用途 |
|---|---|
| `default_data.yaml` | 可选 YAML 覆盖模拟值 |
| `requirements.txt` | Python 依赖 |
| `README.md` | Agent 使用说明（端口、Walk、Trap） |

---

## 不在 test-agent 内的相关目录

| 路径 | 说明 |
|---|---|
| `tools/snmp-agent/` | **旧版** Agent（基于 Exerciser Mibfinal.out），已被 `test-agent/snmp-agent/` 取代，可忽略 |
| `tools/NTCIP-Exerciser/` | 官方 Exerciser 工具（参考用） |
| `tools/readme.txt` | Exerciser / Field Simulator 版本说明 |

---

## 常用命令

```bash
# 启动 Agent（开发）
cd test-agent/snmp-agent
py agent.py --port 1161 --dev-cap 8

# 测试
py -m pytest tests/ -q
py scripts/selftest_1202.py

# 发 Trap
py scripts/trap_send.py --trap-host 127.0.0.1 --type enterprise
```
