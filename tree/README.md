# NTCIP MIB OID 树文档

> 项目文档：[../docs/STRUCTURE.md](../docs/STRUCTURE.md) · 默认值：[../docs/1202DEFAULT_DATA.md](../docs/1202DEFAULT_DATA.md)

本目录包含 MIB 全部定义元素的类型与范围汇总，便于核对模拟数据。

## 文件说明

### 1201 Global (`1201v0227.mib`)

| 文件 | 用途 |
|---|---|
| `1201v0227-tree.txt` | 纯文本树形结构 |
| `1201v0227-tree.md` | Markdown 表格 |
| `1201v0227-flat.csv` | Excel 扁平列表（59 行） |
| `gen_1201_tree.py` | 生成脚本 |

### 1202 ASC (`1202v0218.mib`)

| 文件 | 用途 |
|---|---|
| `1202v0218-tree.txt` | 纯文本树形结构 |
| `1202v0218-tree.md` | Markdown 表格 |
| `1202v0218-flat.csv` | Excel 扁平列表（253 行） |
| `gen_1202_tree.py` | 生成脚本 |

### 通用

| 文件 | 用途 |
|---|---|
| `gen_mib_tree.py` | 通用生成器，支持 `py gen_mib_tree.py 1202v0218.mib` |

## 重新生成

```bash
cd test-agent/tree
py gen_1201_tree.py
py gen_1202_tree.py
# 或
py gen_mib_tree.py 1202v0218.mib
```

## 1201 分支（59 对象）

```
1.3.6.1.4.1.1206
├── 4.1.2.3  profilesPMPP
└── 4.2.6    global
    ├── 1  globalConfiguration
    ├── 2  globalDBManagement
    ├── 3  globalTimeManagement
    └── 7  auxIO
```

## 1202 分支（253 对象）

```
1.3.6.1.4.1.1206.4.2.1  asc
├── 1   phase
├── 2   detector
├── 3   unit
├── 4   coord
├── 5   timebaseAsc
├── 6   preempt
├── 7   ring
├── 8   channel
├── 9   overlap
├── 10  ts2port1
└── 11  ascBlock
```

## 类型说明

| MIB SYNTAX | SNMP 类型 | 典型范围 |
|---|---|---|
| INTEGER (lo..hi) | Integer32 / Gauge32 | lo .. hi（>2³¹ 用 Gauge32） |
| INTEGER { enum } | Integer32 | 枚举值列表 |
| Counter | Counter32 | 0 .. 4294967295 |
| Gauge | Gauge32 | 0 .. 4294967295 |
| OCTET STRING / DisplayString / OwnerString | OctetString | SIZE 约束 |
| OBJECT IDENTIFIER | ObjectIdentifier | 任意 OID |
