# test-agent — NTCIP SNMP 模拟 Agent

独立工程：解析 NTCIP MIB、满填模拟数据、提供 UDP SNMP Agent（Get/Walk/Set/Trap）。

## 快速开始

```bash
cd test-agent/snmp-agent
py -m pip install -r requirements.txt
py agent.py --port 1161 --dev-cap 8
```

MIB Browser：`127.0.0.1:1161`，community `public`，Walk 起点 `1.3.6.1.4.1.1206.4.2`。

## 目录一览

| 目录 | 说明 |
|---|---|
| [docs/](docs/) | **文档**（目录说明、默认值规范） |
| [snmp-agent/](snmp-agent/) | **Agent 源码**（运行入口 `agent.py`） |
| [mibs/mibs_old/](mibs/mibs_old/) | NTCIP MIB 源文件（8004/1103/1201/1202） |
| [tree/](tree/) | OID 树生成工具与导出（md/txt/csv） |
| [reports/](reports/) | 自测报告输出 |

## 文档索引

- [docs/STRUCTURE.md](docs/STRUCTURE.md) — **每个目录/文件用途**
- [docs/DEFAULT_DATA.md](docs/DEFAULT_DATA.md) — 模拟数据总索引
- [docs/1201DEFAULT_DATA.md](docs/1201DEFAULT_DATA.md) — Global (1201) 默认值
- [docs/1202DEFAULT_DATA.md](docs/1202DEFAULT_DATA.md) — ASC (1202) 默认值
- [REQUIREMENTS.md](REQUIREMENTS.md) — 项目需求任务书
- [snmp-agent/README.md](snmp-agent/README.md) — Agent 使用说明
