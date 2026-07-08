#!/usr/bin/env python3
"""Standalone CLI to send a single SNMP trap or inform (v1/v2c/v3)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_AGENT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_AGENT_ROOT))

from trap_sender import default_enterprise_varbinds, send_inform, send_trap  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description="Send NTCIP test SNMP trap or inform")
    p.add_argument("--trap-host", required=True)
    p.add_argument("--trap-port", type=int, default=162)
    p.add_argument("--trap-community", default="public")
    p.add_argument(
        "--type",
        choices=["coldStart", "warmStart", "enterprise"],
        default="enterprise",
    )
    p.add_argument("--version", choices=["v1", "v2c", "v3"], default="v2c")
    p.add_argument(
        "--inform",
        action="store_true",
        help="Send SNMP Inform instead of Trap",
    )
    p.add_argument("--v3-user", default=None, help="SNMPv3 USM user (required for --version v3)")
    p.add_argument("--v3-auth-key", default=None, help="SNMPv3 auth passphrase")
    p.add_argument("--v3-priv-key", default=None, help="SNMPv3 priv passphrase (optional)")
    p.add_argument("--v3-auth-proto", choices=["md5", "sha"], default="md5")
    p.add_argument("--v3-priv-proto", choices=["des", "aes"], default="des")
    args = p.parse_args()

    if args.version == "v3" and not args.v3_user:
        print("error: --version v3 requires --v3-user", file=sys.stderr)
        sys.exit(2)

    varbinds = default_enterprise_varbinds() if args.type == "enterprise" else None
    sender = send_inform if args.inform else send_trap
    ok = sender(
        args.type,
        args.trap_host,
        args.trap_port,
        args.trap_community,
        snmp_version=args.version,
        varbinds=varbinds,
        v3_user=args.v3_user,
        v3_auth_key=args.v3_auth_key,
        v3_priv_key=args.v3_priv_key,
        v3_auth_proto=args.v3_auth_proto,
        v3_priv_proto=args.v3_priv_proto,
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
