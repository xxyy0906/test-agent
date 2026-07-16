# Ubuntu 环境启动指南

在 Ubuntu 上安装依赖并启动 NTCIP SNMP 模拟 Agent。

> Windows 快速开始见 [../README.md](../README.md)；Agent 参数见 [../snmp-agent/README.md](../snmp-agent/README.md)。

## 环境要求

| 项目 | 说明 |
|---|---|
| 系统 | Ubuntu 20.04 / 22.04 / 24.04（或其他带 Python 3.9+ 的发行版） |
| Python | **3.9+**（推荐系统自带 `python3`） |
| 网络 | Agent 默认监听 `0.0.0.0`；本机测试用 `127.0.0.1`，局域网用本机 IP |

## 1. 安装系统依赖

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

可选（命令行 SNMP 客户端，用于冒烟验证）：

```bash
sudo apt install -y snmp
```

## 2. 获取代码并进入目录

将 `test-agent` 拷贝或克隆到 Ubuntu 后：

```bash
cd /path/to/test-agent/snmp-agent
```

## 3. 创建虚拟环境并安装 Python 依赖

> **必须在 `snmp-agent/` 目录下操作**（`requirements.txt` 与 `agent.py` 都在这里，不在上一级 `test-agent/`）。

若之前装失败过，先删掉旧 venv 再重建：

```bash
cd /path/to/test-agent/snmp-agent
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U "pip>=24" setuptools wheel
python3 -m pip install -r requirements.txt
```

若下载 `files.pythonhosted.org` 超时，见第 9 节「PyPI 超时」。

之后每次新开终端，先执行：

```bash
cd /path/to/test-agent/snmp-agent
source .venv/bin/activate
```

## 4. 启动 Agent

**推荐：用一键脚本（自动找 `.venv`，161 端口自动 `sudo .venv/bin/python`）**

```bash
cd /path/to/test-agent/snmp-agent
chmod +x start_ubuntu.sh    # 仅首次需要
./start_ubuntu.sh           # 默认 --port 1161 --dev-cap 8
./start_ubuntu.sh --port 161
./start_ubuntu.sh --full    # 满填（不加 --dev-cap）
./start_ubuntu.sh --help
```

Windows 请用同目录下的 `start_windows.bat`。

或手动启动。**推荐：非特权端口 1161（无需 root）**

```bash
# 开发模式（表维度 cap=8，启动更快）
python3 agent.py --port 1161 --dev-cap 8

# 满填（OID 实例较多，启动较慢、占内存）
python3 agent.py --port 1161
```

成功时终端类似：

```
SNMP Agent listening on 0.0.0.0:1161
  Operations: Get, GetNext, GetBulk, Set
  Protocols:  SNMP v1/v2c
  Community (rw): 'public'
```

按 `Ctrl+C` 停止。

### 使用标准端口 161

UDP 161 为特权端口，普通用户无法绑定。依赖装在 `.venv` 里，**不要**用 `sudo python3`（那是系统 Python，会报 `No module named 'pysnmp'`）。

```bash
# 须先 cd 到 snmp-agent/，且已创建并安装过 .venv

# 方式 A：用 venv 里的解释器以 root 运行（仅测试环境）
sudo .venv/bin/python agent.py --port 161 --dev-cap 8

# 方式 B：给 venv 的 python 提权后，普通用户运行（推荐）
sudo setcap 'cap_net_bind_service=+ep' "$(readlink -f .venv/bin/python)"
source .venv/bin/activate
python3 agent.py --port 161 --dev-cap 8
```

> 若本机已有 `snmpd` 占用 161，先停掉：`sudo systemctl stop snmpd`。  
> 防火墙需放行：`sudo ufw allow 161/udp`。MIB Browser 端口填 **161**。

## 5. 验证

另开一个终端（同样 `source .venv/bin/activate`）：

```bash
# 若已安装 net-snmp 客户端
snmpget -v2c -c public 127.0.0.1:1161 1.3.6.1.4.1.1206.4.2.1.1.1.0

# 或用工程脚本
python3 scripts/snmp_get_test.py --port 1161
```

MIB Browser / 管理站配置：

| 项 | 值 |
|---|---|
| 地址 | `127.0.0.1`（本机）或 Ubuntu 主机局域网 IP |
| 端口 | `1161`（或你启动时指定的端口） |
| Community | `public` |
| Walk 起点 | `1.3.6.1.4.1.1206.4.2` |

## 6. 防火墙（仅局域网访问时需要）

```bash
# ufw 示例：放行 UDP 1161
sudo ufw allow 1161/udp
sudo ufw status
```

## 7. 常用命令对照

| 用途 | Ubuntu |
|---|---|
| 一键启动（开发） | `./start_ubuntu.sh` |
| 一键启动（161） | `./start_ubuntu.sh --port 161` |
| 启动（开发） | `python3 agent.py --port 1161 --dev-cap 8` |
| 启动（满填） | `./start_ubuntu.sh --full` 或 `python3 agent.py --port 1161` |
| 发 Trap | `python3 scripts/trap_send.py --trap-host 127.0.0.1 --type enterprise` |
| 单元测试 | `python3 -m pytest tests/ -q` |
| Get 冒烟 | `python3 scripts/snmp_get_test.py --port 1161` |
| Set 冒烟 | `python3 scripts/snmp_set_test.py --port 1161` |

Windows 上常用 `py`；Ubuntu 请用 **`python3`**（或虚拟环境里的 `python`）。

## 8. 后台运行（可选）

用 `systemd` 用户服务或 `nohup`：

```bash
# 简单后台
nohup python3 agent.py --port 1161 --dev-cap 8 > agent.log 2>&1 &
```

或编写 `/etc/systemd/system/ntcip-snmp-agent.service`（按实际路径修改）：

```ini
[Unit]
Description=NTCIP SNMP Test Agent
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/test-agent/snmp-agent
ExecStart=/path/to/test-agent/snmp-agent/.venv/bin/python agent.py --port 1161 --dev-cap 8
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ntcip-snmp-agent
sudo systemctl status ntcip-snmp-agent
```

## 9. 常见问题

| 现象 | 处理 |
|---|---|
| `Cannot bind UDP ...:161` / Permission denied | 改用 `--port 1161`，或见上文「使用标准端口 161」 |
| 端口已被占用 | `ss -ulnp \| grep 1161`，换端口或结束占用进程 |
| 远程 Get 超时 | 检查 `ufw`/防火墙、Agent 是否监听 `0.0.0.0`、客户端是否写对端口（1161 vs 161） |
| 本机 Wireshark 抓不到 Get | 本机访问本机 IP 不走物理网卡，抓 **lo**（loopback）；Trap 发往其他主机时可在物理网卡上看到 |
| `No such file ... requirements.txt` / `can't open file 'agent.py'` | 当前不在 `snmp-agent/`：`cd ~/…/test-agent/snmp-agent` |
| `Read timed out` / `files.pythonhosted.org` | 访问官方 PyPI 超时（国内常见）。用国内镜像重装，见下方「PyPI 超时」 |
| `ResolutionImpossible` / `pysmi-lextudio`/`requests` 冲突 | 拉取最新代码（`requirements.txt` 已钉死与 Windows 一致的版本），删 `.venv` 后按第 3 节重装；并确保 `pip>=24` |
| `ModuleNotFoundError: pysnmp`（`sudo python3` 后） | `sudo` 走了系统 Python。改用 `sudo .venv/bin/python agent.py ...`，见「使用标准端口 161」 |
| `ModuleNotFoundError: pyasn1` / `pysnmp`（未 sudo） | 依赖未装成功；激活 venv 后重新 `pip install -r requirements.txt` |
| Python 3.8 / `python3 --version` 显示 3.8 | 本工程要求 **3.9+**。Ubuntu 20.04 请装 `python3.9`/`python3.10` 后用对应解释器建 venv |

### PyPI 超时（`Read timed out` / `files.pythonhosted.org`）

删掉半截 venv，用国内镜像重装（清华源示例，可换成阿里云等）：

```bash
cd ~/develop/ntcip-snmp-agent/test-agent/snmp-agent
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate

# 先确认版本（需 3.9+）
python3 --version

export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
export PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn
export PIP_DEFAULT_TIMEOUT=120

python3 -m pip install -U "pip>=24" setuptools wheel
python3 -m pip install -r requirements.txt
python3 agent.py --port 1161 --dev-cap 8
```

等价写法（不设环境变量）：

```bash
python3 -m pip install -U "pip>=24" setuptools wheel \
  -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
python3 -m pip install -r requirements.txt \
  -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

其他常用镜像：`https://mirrors.aliyun.com/pypi/simple/`、`https://pypi.douban.com/simple/`。

## 相关文档

- [../README.md](../README.md) — 项目入口
- [../snmp-agent/README.md](../snmp-agent/README.md) — Agent 参数与 Set/Trap
- [STRUCTURE.md](STRUCTURE.md) — 目录说明
- [../REQUIREMENTS.md](../REQUIREMENTS.md) — 需求任务书
