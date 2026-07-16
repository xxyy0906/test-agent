#!/usr/bin/env python3
"""NTCIP UDP SNMP Agent — Get / GetNext / GetBulk / Set / Trap / Inform."""
from __future__ import annotations

import argparse
import asyncio
import logging
import sys
import threading
import time
from pathlib import Path

try:
    from pyasn1.compat.octets import null
except ImportError:  # pyasn1 >= 0.6.1 removed compat.octets
    null = b""
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity import config, engine
from pysnmp.entity.rfc3413 import cmdrsp, context

from instrum import FlatMibInstrum
from mib_loader import MibLoader
from oid_utils import DEVICES_OID_ROOT, oid_dotted, parse_oid_root
from trap_sender import default_enterprise_varbinds, send_inform, send_trap

DEFAULT_OID_ROOT = oid_dotted(DEVICES_OID_ROOT)
DEFAULT_MIB_DIR = Path(__file__).resolve().parent.parent / "mibs" / "mibs_old"
DEFAULT_DATA = Path(__file__).resolve().parent / "default_data.yaml"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="NTCIP SNMP agent — Get, GetNext, GetBulk, Set, Trap, Inform"
    )
    p.add_argument("--mib-dir", type=Path, default=DEFAULT_MIB_DIR)
    p.add_argument("--default-data", type=Path, default=DEFAULT_DATA)
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=161)
    p.add_argument("--community", default="public", help="Read-write community (v1/v2c)")
    p.add_argument(
        "--community-ro",
        default=None,
        help="Optional read-only community (Get/Walk only, Set rejected)",
    )
    p.add_argument("--oid-root", default=DEFAULT_OID_ROOT)
    p.add_argument("--all-ntcip", action="store_true")
    p.add_argument("--dev-cap", type=int, default=None)
    p.add_argument("--trap-host", default=None)
    p.add_argument("--trap-port", type=int, default=162)
    p.add_argument("--trap-community", default="public")
    p.add_argument("--trap-interval", type=int, default=0)
    p.add_argument(
        "--send-trap",
        choices=["coldStart", "warmStart", "enterprise"],
        default=None,
    )
    p.add_argument(
        "--send-inform",
        choices=["coldStart", "warmStart", "enterprise"],
        default=None,
        help="Send one SNMP Inform at startup (v2c, expects Response)",
    )
    # SNMPv3 (optional)
    p.add_argument("--v3-user", default=None, help="SNMPv3 USM user name")
    p.add_argument("--v3-auth-key", default=None, help="SNMPv3 auth passphrase")
    p.add_argument("--v3-priv-key", default=None, help="SNMPv3 priv passphrase (optional)")
    p.add_argument(
        "--v3-auth-proto",
        choices=["md5", "sha"],
        default="md5",
    )
    p.add_argument(
        "--v3-priv-proto",
        choices=["des", "aes"],
        default="des",
    )
    p.add_argument("--verbose", action="store_true")
    return p


def _trap_loop(host: str, port: int, community: str, interval: int) -> None:
    while True:
        send_trap("enterprise", host, port, community, varbinds=default_enterprise_varbinds())
        time.sleep(interval)


def _setup_snmp_v3(snmp_engine, args) -> None:
    auth_proto = (
        config.usmHMACSHAAuthProtocol
        if args.v3_auth_proto == "sha"
        else config.usmHMACMD5AuthProtocol
    )
    priv_proto = (
        config.usmAesCfb128Protocol
        if args.v3_priv_proto == "aes"
        else config.usmDESPrivProtocol
    )
    config.addV3User(
        snmp_engine,
        args.v3_user,
        auth_proto,
        args.v3_auth_key,
        priv_proto if args.v3_priv_key else config.usmNoPrivProtocol,
        args.v3_priv_key,
    )


def main() -> None:
    args = build_parser().parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, OSError):
        pass

    mib_dir = args.mib_dir.resolve()
    if not mib_dir.is_dir():
        print(f"MIB directory not found: {mib_dir}", file=sys.stderr)
        sys.exit(1)

    default_data = args.default_data.resolve() if args.default_data else None
    if default_data and not default_data.is_file():
        default_data = None

    print(f"Loading MIBs from: {mib_dir}")
    oid_root = None if args.all_ntcip else parse_oid_root(args.oid_root)
    if oid_root:
        print(f"OID scope: {oid_dotted(oid_root)} (devices subtree)")
    else:
        print("OID scope: full NTCIP (1.3.6.1.4.1.1206)")

    loader = MibLoader(
        mib_dir,
        default_data_path=default_data,
        dev_cap=args.dev_cap,
        oid_root=oid_root,
    )
    oid_values = loader.load()
    print(f"OID instances loaded: {loader.stats.get('total', len(oid_values))}")
    print(f"OID registry entries: {len(loader.oid_registry)}")

    write_communities = {args.community}
    write_v3_users: set[str] = set()
    if args.v3_user:
        write_v3_users.add(args.v3_user)

    if args.trap_host and args.send_trap:
        ok = send_trap(
            args.send_trap,
            args.trap_host,
            args.trap_port,
            args.trap_community,
            varbinds=default_enterprise_varbinds() if args.send_trap == "enterprise" else None,
        )
        print(f"Startup trap '{args.send_trap}': {'OK' if ok else 'FAILED'}")

    if args.trap_host and args.send_inform:
        ok = send_inform(
            args.send_inform,
            args.trap_host,
            args.trap_port,
            args.trap_community,
            varbinds=default_enterprise_varbinds() if args.send_inform == "enterprise" else None,
        )
        print(f"Startup inform '{args.send_inform}': {'OK' if ok else 'FAILED'}")

    if args.trap_host and args.trap_interval > 0:
        t = threading.Thread(
            target=_trap_loop,
            args=(args.trap_host, args.trap_port, args.trap_community, args.trap_interval),
            daemon=True,
        )
        t.start()
        print(f"Periodic trap every {args.trap_interval}s -> {args.trap_host}:{args.trap_port}")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    snmp_engine = engine.SnmpEngine()
    try:
        config.addTransport(
            snmp_engine,
            udp.domainName + (1,),
            udp.UdpTransport().openServerMode((args.host, args.port)),
        )
    except OSError as exc:
        print(
            f"Cannot bind UDP {args.host}:{args.port} ({exc}). "
            "Use --port 1161 or run as Administrator.",
            file=sys.stderr,
        )
        sys.exit(2)

    config.addV1System(snmp_engine, "rw-area", args.community)
    # VACM: allow read/write on NTCIP subtree (required for UDP Set)
    vacm_root = oid_root if oid_root else (1, 3, 6, 1, 4, 1, 1206)
    for sec_model in (1, 2):
        config.addRwUser(
            snmp_engine,
            sec_model,
            "rw-area",
            "noAuthNoPriv",
            vacm_root,
        )
    if args.community_ro:
        config.addV1System(snmp_engine, "ro-area", args.community_ro)
        for sec_model in (1, 2):
            config.addRoUser(
                snmp_engine,
                sec_model,
                "ro-area",
                "noAuthNoPriv",
                vacm_root,
            )

    if args.v3_user and args.v3_auth_key:
        _setup_snmp_v3(snmp_engine, args)
        print(f"SNMPv3 user '{args.v3_user}' enabled ({args.v3_auth_proto}/{args.v3_priv_proto})")

    instrum = FlatMibInstrum(
        oid_values,
        registry=loader.oid_registry,
        write_communities=write_communities,
        write_v3_users=write_v3_users,
    )

    # Startup smoke: scalar + table column must respond
    from pysnmp.proto import rfc1902

    _smoke = [
        (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 8, 1, 0),
        (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 8, 2, 1, 2, 1),
    ]
    for oid in _smoke:
        _, val = instrum.readVars([(rfc1902.ObjectName(oid), None)])[0]
        if val.__class__.__name__ == "noSuchObject":
            print(f"WARNING: no default for {'.'.join(map(str, oid))}", file=sys.stderr)

    snmp_context = context.SnmpContext(snmp_engine)
    snmp_context.contextNames[null] = instrum

    # All agent-side SNMP PDU handlers (RFC 3413)
    cmdrsp.GetCommandResponder(snmp_engine, snmp_context)
    cmdrsp.NextCommandResponder(snmp_engine, snmp_context)
    cmdrsp.BulkCommandResponder(snmp_engine, snmp_context)
    cmdrsp.SetCommandResponder(snmp_engine, snmp_context)

    ops = "Get, GetNext, GetBulk, Set"
    protos = "SNMP v1/v2c"
    if args.v3_user:
        protos += "/v3"
    print(f"SNMP Agent listening on {args.host}:{args.port}")
    print(f"  Operations: {ops}")
    print(f"  Protocols:  {protos}")
    print(f"  Community (rw): '{args.community}'")
    if args.community_ro:
        print(f"  Community (ro): '{args.community_ro}' (Set disabled)")
    print(f"  Table/scalar instances loaded (incl. channelTable rows)")
    print(f"  Smoke test: maxChannels + channelControlSource.1 OK")

    try:
        snmp_engine.transportDispatcher.runDispatcher()
    except KeyboardInterrupt:
        pass
    finally:
        snmp_engine.transportDispatcher.closeDispatcher()


if __name__ == "__main__":
    main()
