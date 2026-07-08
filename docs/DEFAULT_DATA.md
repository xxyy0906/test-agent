# DEFAULT_DATA.md — NTCIP SNMP Agent 模拟数据索引

**默认 Agent OID 范围：`1.3.6.1.4.1.1206.4.2`（devices 子树）**

| 分支 | OID | MIB | 默认值文档 |
|---|---|---|---|
| ASC | `…4.2.1` | NTCIP 1202 | **[1202DEFAULT_DATA.md](1202DEFAULT_DATA.md)** |
| Global | `…4.2.6` | NTCIP 1201 + 1103 | **[1201DEFAULT_DATA.md](1201DEFAULT_DATA.md)** |
| 其他设备 | `…4.2.2`～`.5`、`.7`～`.13` | 8004 树节点 | 无管理对象 |

## 全局策略（两 MIB 共用）

| 规则 | 说明 |
|---|---|
| 解析器 | `snmp-agent/sim_data/resolver.py` |
| 表展开 | 按 MIB `max*` scalar 或 INDEX 列 INTEGER 范围上限满行 |
| Scalar 实例 | 定义 OID + `.0` |
| INTEGER (lo..hi) | 非 INDEX 取 **hi**；INDEX 取行号 |
| INTEGER { enum } | 取最大 enum；有 DEFVAL 优先 DEFVAL |
| Counter / Gauge | Counter32 / Gauge32 上限 |
| OCTET STRING | DEFVAL 空串或 SIZE 填充 |
| ObjectIdentifier | 默认指向 ASC `1.3.6.1.4.1.1206.4.2.1` |
| YAML 覆盖 | `snmp-agent/default_data.yaml` |

## Trap VarBind 默认值

enterprise Trap 附加 VarBind（`trap_sender.default_enterprise_varbinds()`）：

| OID | 值 | 含义 |
|---|---|---|
| eventLogClass.1 | 1 | 事件类 |
| eventLogNumber.1 | 1 | 类内序号 |
| eventLogTime.1 | 1000 | 模拟时间 Counter |

## 扩展 OID 范围

```bash
py agent.py --all-ntcip          # 整个 1.3.6.1.4.1.1206
py agent.py --oid-root 1.3.6.1.4.1.1206.4.2.1   # 仅 ASC
```
