#!/usr/bin/env python3
"""SNMP Set smoke / full test against running UDP agent."""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

_AGENT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_AGENT_ROOT))

from mib_loader import MibLoader  # noqa: E402
from oid_utils import DEVICES_OID_ROOT  # noqa: E402
from sim_data.set_values import (  # noqa: E402
    SetTestCase,
    alternate_set_value,
    collect_writable_set_cases,
    invalid_set_value,
)

from pysnmp.hlapi.asyncio import (  # noqa: E402
    CommunityData,
    ContextData,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    getCmd,
    setCmd,
)
from pysnmp.proto import rfc1902  # noqa: E402

SMOKE: list[tuple[str, str]] = [
    ("unitControl (scalar)", "1.3.6.1.4.1.1206.4.2.1.3.10.0"),
    ("phasePedestrianClear.1", "1.3.6.1.4.1.1206.4.2.1.1.2.1.3.1"),
    ("channelControlSource.1", "1.3.6.1.4.1.1206.4.2.1.8.2.1.2.1"),
    ("splitTime.1.1 (dual)", "1.3.6.1.4.1.1206.4.2.1.4.9.1.3.1.1"),
    ("maxPhases (read-only reject)", "1.3.6.1.4.1.1206.4.2.1.1.1.0"),
]

READONLY_SMOKE_OID = "1.3.6.1.4.1.1206.4.2.1.1.1.0"


def _oid_tuple(text: str) -> tuple[int, ...]:
    return tuple(int(x) for x in text.strip().lstrip(".").split("."))


async def _get(engine, target, comm, oid: str):
    err, err_status, _, vb = await getCmd(
        engine, comm, target, ContextData(), ObjectType(ObjectIdentity(oid))
    )
    if err or err_status or not vb:
        return err or f"errorStatus={err_status}", None, None
    name, val = vb[0]
    return None, name.prettyPrint(), val


async def _set(engine, target, comm, oid: str, val):
    err, err_status, err_index, vb = await setCmd(
        engine,
        comm,
        target,
        ContextData(),
        ObjectType(ObjectIdentity(oid), val),
    )
    if err:
        return err, err_status, None, None
    if err_status:
        return None, err_status, None, None
    if not vb:
        return "empty response", err_status, None, None
    name, val_out = vb[0]
    return None, err_status, name.prettyPrint(), val_out


def _val_pretty(val) -> str:
    if val is None:
        return ""
    if type(val).__name__ == "OctetString":
        raw = bytes(val)
        try:
            return repr(raw.decode("ascii"))
        except UnicodeDecodeError:
            return raw.hex()
    return val.prettyPrint()


def _snmp_error_status(err_status) -> str | None:
    if err_status is None or err_status == 0:
        return None
    text = getattr(err_status, "prettyPrint", lambda: str(err_status))()
    return text


async def _run_case(
    engine,
    target,
    comm,
    label: str,
    oid: str,
    syntax: str,
    *,
    expect_reject: bool = False,
) -> bool:
    err, _, old_val = await _get(engine, target, comm, oid)
    if err:
        print(f"FAIL {label}: Get error {err}")
        return False
    if old_val is None:
        print(f"FAIL {label}: empty Get")
        return False

    if expect_reject:
        new_val = rfc1902.Integer32(1)
        err, err_status, _, _ = await _set(engine, target, comm, oid, new_val)
        if err:
            print(f"FAIL {label}: Set transport error {err}")
            return False
        es = _snmp_error_status(err_status)
        if es in ("notWritable", "noAccess", "wrongValue", "noSuchName"):
            print(f"OK   {label}: Set rejected (errorStatus={es})")
            return True
        print(f"FAIL {label}: read-only Set succeeded (errorStatus={es})")
        return False

    try:
        new_val = alternate_set_value(syntax, old_val)
    except Exception as exc:
        print(f"FAIL {label}: cannot build alt value: {exc}")
        return False

    err, err_status, set_name, set_val = await _set(engine, target, comm, oid, new_val)
    if err:
        print(f"FAIL {label}: Set error {err}")
        return False
    es = _snmp_error_status(err_status)
    if es:
        print(f"FAIL {label}: Set errorStatus={es}")
        return False

    err, _, got = await _get(engine, target, comm, oid)
    if err:
        print(f"FAIL {label}: read-back Get error {err}")
        return False
    if _val_pretty(got) != _val_pretty(set_val):
        print(f"FAIL {label}: read-back mismatch got={_val_pretty(got)} expected={_val_pretty(set_val)}")
        return False

    print(f"OK   {label}: Set {_val_pretty(old_val)} -> {_val_pretty(set_val)}")
    print(f"     rsp OID: {set_name}")
    return True


async def _run_all(
    host: str,
    port: int,
    community: str,
    cases: list[tuple[str, str, str, bool]],
) -> int:
    engine = SnmpEngine()
    target = UdpTransportTarget((host, port), timeout=3, retries=1)
    comm = CommunityData(community, mpModel=1)
    failed = 0
    for label, oid, syntax, reject in cases:
        ok = await _run_case(engine, target, comm, label, oid, syntax, expect_reject=reject)
        if not ok:
            failed += 1
    engine.transportDispatcher.closeDispatcher()
    return failed


def _full_cases() -> list[tuple[str, str, str, bool]]:
    loader = MibLoader(_AGENT_ROOT.parent / "mibs" / "mibs_old", dev_cap=8, oid_root=DEVICES_OID_ROOT)
    loader.load()
    reg = loader.oid_registry
    cases: list[tuple[str, str, str, bool]] = []
    for c in collect_writable_set_cases(reg):
        oid = ".".join(str(x) for x in c.instance_oid)
        cases.append((c.name, oid, c.syntax, False))
    cases.append(("maxPhases (read-only)", READONLY_SMOKE_OID, "INTEGER", True))
    return cases


def main() -> int:
    p = argparse.ArgumentParser(description="SNMP Set test (SET version)")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=1161)
    p.add_argument("--community", default="public")
    p.add_argument("--full", action="store_true", help="Test all 137 writable objects")
    args = p.parse_args()

    loader = MibLoader(_AGENT_ROOT.parent / "mibs" / "mibs_old", dev_cap=8, oid_root=DEVICES_OID_ROOT)
    loader.load()
    syntax_by_name = {m.name: m.syntax for m in loader.oid_registry.values()}

    if args.full:
        cases = []
        for c in collect_writable_set_cases(loader.oid_registry):
            oid = ".".join(str(x) for x in c.instance_oid)
            cases.append((c.name, oid, c.syntax, False))
        cases.append(("maxPhases (read-only)", READONLY_SMOKE_OID, "INTEGER", True))
    else:
        cases = []
        for label, oid in SMOKE:
            reject = oid == READONLY_SMOKE_OID
            name = label.split()[0]
            syntax = syntax_by_name.get(name, "INTEGER (0..255)")
            cases.append((label, oid, syntax, reject))

    failed = asyncio.run(_run_all(args.host, args.port, args.community, cases))
    if failed:
        print(f"\n{failed} failed — ensure agent: py agent.py --port {args.port} --dev-cap 8")
        return 1
    print(f"\nAll OK ({len(cases)} cases, SET UDP test)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
