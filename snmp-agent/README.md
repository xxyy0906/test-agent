# SNMP Agent 使用说明

独立 NTCIP SNMP 模拟 Agent，**默认只填充并响应** `1.3.6.1.4.1.1206.4.2`（devices 子树）。

> 项目总览：[../README.md](../README.md) · 目录说明：[../docs/STRUCTURE.md](../docs/STRUCTURE.md)

## 目录结构（本工程）

```
snmp-agent/
├── agent.py              启动 Agent
├── mib_loader.py         MIB 加载与表展开
├── instrum.py            SNMP Get/Set 实现
├── sim_data/             模拟数据规则
├── scripts/
│   ├── trap_send.py      发送 Trap/Inform
│   ├── selftest_1202.py  1202 Get/默认值自测
│   ├── selftest_1202_set.py  **1202 SET 全量自测（SET 版）**
│   ├── snmp_get_test.py  UDP Get 冒烟
│   └── snmp_set_test.py  **UDP Set 冒烟/全量（SET 版）**
├── tests/                单元测试
├── deps/                 RFC 依赖 MIB
└── default_data.yaml     可选覆盖
```

## 安装与启动

**Windows**（`start_windows.bat` 或 `py`）：

```bash
cd test-agent/snmp-agent
start_windows.bat                     # 默认 1161 + --dev-cap 8
# 或
py -m pip install -r requirements.txt
py agent.py --port 1161 --dev-cap 8   # 开发模式
py agent.py --port 1161               # 满填
```

**Ubuntu**：完整步骤见 [../docs/UBUNTU.md](../docs/UBUNTU.md)。摘要：

```bash
cd test-agent/snmp-agent
rm -rf .venv && python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -U "pip>=24" setuptools wheel
python3 -m pip install -r requirements.txt
chmod +x start_ubuntu.sh && ./start_ubuntu.sh   # 默认 1161 + --dev-cap 8
# ./start_ubuntu.sh --port 161                  # 特权端口（自动 sudo .venv python）
```

## MIB Browser

- 地址：`127.0.0.1:1161`，community `public`
- Walk 起点：`1.3.6.1.4.1.1206.4.2`
- 支持 Get / GetNext / GetBulk / **Set（read-write，方案 A 进程内读回）** / Trap / Inform（v1/v2c/v3）

双击 Get 兼容：
- **标量** `…1.1.0`：省略 `.0` 时自动补全
- **表列** `…8.2.1.1`：自动补 **table key 第 1 行** → `…8.2.1.1.1`，响应返回完整实例 OID
- **表节点** `…8.2.1.2`：返回该表下第一个实例

## 脚本

```bash
py scripts/trap_send.py --trap-host 127.0.0.1 --type enterprise
py scripts/selftest_1202.py              # Get/默认值（原版）
py scripts/selftest_1202_set.py          # SET 全量自测 → reports/1202-set-selftest-report.md
py scripts/snmp_get_test.py --port 1161
py scripts/snmp_set_test.py --port 1161           # SET 冒烟（5 条）
py scripts/snmp_set_test.py --port 1161 --full    # SET 全量（137 可写对象）
py -m pytest tests/ -q
```

### Set 说明（SET 版 / 方案 A）

- 所有 `read-write` 标量/表列可 Set；`read-only` / INDEX 拒绝
- Set 后同进程 Get/Walk 读回新值；**重启 Agent 恢复默认**（不持久化到文件）
- OID 补全规则与 Get 相同（标量 `.0`、表列补第 1 行）

## 文档

- [../docs/1201DEFAULT_DATA.md](../docs/1201DEFAULT_DATA.md) — Global (1201)
- [../docs/1202DEFAULT_DATA.md](../docs/1202DEFAULT_DATA.md) — ASC (1202)
- [../docs/DEFAULT_DATA.md](../docs/DEFAULT_DATA.md) — 模拟数据索引
- [../REQUIREMENTS.md](../REQUIREMENTS.md) — 需求任务书
