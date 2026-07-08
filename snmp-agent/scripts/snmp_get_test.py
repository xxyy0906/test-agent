#!/usr/bin/env python3
"""Quick SNMP Get test against running agent (scalar + table column)."""
from __future__ import annotations

import argparse
import asyncio
import sys

from pysnmp.hlapi.asyncio import (
    CommunityData,
    ContextData,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    getCmd,
)

SAMPLES = [
    ("maxChannels (scalar)", "1.3.6.1.4.1.1206.4.2.1.8.1.0"),
    ("channelNumber.1", "1.3.6.1.4.1.1206.4.2.1.8.2.1.1.1"),
    ("channelControlSource (col)", "1.3.6.1.4.1.1206.4.2.1.8.2.1.2"),
    ("channelControlSource.1", "1.3.6.1.4.1.1206.4.2.1.8.2.1.2.1"),
    ("channelControlType.1", "1.3.6.1.4.1.1206.4.2.1.8.2.1.3.1"),
]


async def _run(host: str, port: int, community: str, oids: list[tuple[str, str]]) -> int:
    engine = SnmpEngine()
    target = UdpTransportTarget((host, port), timeout=3, retries=1)
    comm = CommunityData(community, mpModel=1)
    failed = 0
    for label, oid in oids:
        err, _, _, vb = await getCmd(
            engine, comm, target, ContextData(), ObjectType(ObjectIdentity(oid))
        )
        if err or not vb:
            print(f"FAIL {label}: {oid}  ({err or 'empty'})")
            failed += 1
        else:
            name, val = vb[0]
            print(f"OK   {label}: req={oid}")
            print(f"     rsp={name.prettyPrint()} = {val.prettyPrint()}")
    engine.transportDispatcher.closeDispatcher()
    return failed


def main() -> int:
    p = argparse.ArgumentParser(description="SNMP Get smoke test")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=1161)
    p.add_argument("--community", default="public")
    p.add_argument("--oid", action="append", default=[], help="Extra OID to Get")
    args = p.parse_args()
    oids = list(SAMPLES)
    for extra in args.oid:
        oids.append((extra, extra))
    failed = asyncio.run(_run(args.host, args.port, args.community, oids))
    if failed:
        print(f"\n{failed} failed — no SNMP response on {args.host}:{args.port}")
        print("  1. Start agent (keep terminal open): py agent.py --port 1161 --dev-cap 8")
        print("  2. If bind fails or still timeout, kill stale process on this port:")
        print("       netstat -ano | findstr :1161")
        print("       taskkill /PID <pid> /F")
        print("     (old tools\\snmp-agent on 1161 often hangs and must be killed)")
        return 1
    print("\nAll OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
