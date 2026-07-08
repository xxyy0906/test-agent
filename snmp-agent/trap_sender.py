"""Send SNMP v1/v2c/v3 traps and informs for NTCIP agent testing."""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Literal

from pysnmp.hlapi.asyncio import (
    CommunityData,
    ContextData,
    NotificationType,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    UsmUserData,
    sendNotification,
    usmAesCfb128Protocol,
    usmDESPrivProtocol,
    usmHMACMD5AuthProtocol,
    usmHMACSHAAuthProtocol,
    usmNoAuthProtocol,
    usmNoPrivProtocol,
)
from pysnmp.proto import rfc1902

from sim_data.default_values import ENTERPRISE_OID

log = logging.getLogger(__name__)

TrapType = Literal["coldStart", "warmStart", "enterprise"]
NotifyKind = Literal["trap", "inform"]
SnmpVersion = Literal["v1", "v2c", "v3"]

STANDARD_TRAP_OIDS = {
    "coldStart": "1.3.6.1.6.3.1.1.5.1",
    "warmStart": "1.3.6.1.6.3.1.1.5.2",
}


@dataclass(frozen=True)
class V3Credentials:
    user: str
    auth_key: str | None = None
    priv_key: str | None = None
    auth_proto: str = "md5"
    priv_proto: str = "des"


def build_usm_user(creds: V3Credentials) -> UsmUserData:
    """Build USM credentials for SNMPv3 trap/inform."""
    if creds.auth_key:
        auth_protocol = (
            usmHMACSHAAuthProtocol if creds.auth_proto == "sha" else usmHMACMD5AuthProtocol
        )
    else:
        auth_protocol = usmNoAuthProtocol

    if creds.priv_key:
        priv_protocol = (
            usmAesCfb128Protocol if creds.priv_proto == "aes" else usmDESPrivProtocol
        )
    else:
        priv_protocol = usmNoPrivProtocol

    return UsmUserData(
        creds.user,
        authKey=creds.auth_key,
        privKey=creds.priv_key,
        authProtocol=auth_protocol,
        privProtocol=priv_protocol,
    )


def _build_auth(
    snmp_version: SnmpVersion,
    community: str,
    v3: V3Credentials | None,
):
    if snmp_version == "v3":
        if not v3 or not v3.user:
            raise ValueError("SNMPv3 requires --v3-user (and usually --v3-auth-key)")
        return build_usm_user(v3)
    return CommunityData(community, mpModel=1 if snmp_version == "v2c" else 0)


async def _send_notification_async(
    trap_type: TrapType,
    host: str,
    port: int,
    community: str,
    snmp_version: SnmpVersion,
    enterprise_subid: int,
    varbinds: list[tuple[str, object]] | None,
    notify_kind: NotifyKind,
    v3: V3Credentials | None = None,
) -> bool:
    engine = SnmpEngine()
    target = UdpTransportTarget((host, port), timeout=2, retries=1)
    auth = _build_auth(snmp_version, community, v3)

    if trap_type in STANDARD_TRAP_OIDS:
        notification = NotificationType(ObjectIdentity(STANDARD_TRAP_OIDS[trap_type]))
    else:
        trap_oid = f"{ENTERPRISE_OID}.0.{enterprise_subid}"
        notification = NotificationType(ObjectIdentity(trap_oid))

    if varbinds:
        for oid, val in varbinds:
            notification = notification.addVarBinds(ObjectType(ObjectIdentity(oid), val))

    error_indication, _, _, _ = await sendNotification(
        engine,
        auth,
        target,
        ContextData(),
        notify_kind,
        notification,
    )
    engine.transportDispatcher.closeDispatcher()
    if error_indication:
        log.error("%s send failed: %s", notify_kind, error_indication)
        return False
    log.info(
        "%s %s (%s) sent to %s:%s",
        notify_kind,
        trap_type,
        snmp_version,
        host,
        port,
    )
    return True


async def _send_trap_async(
    trap_type: TrapType,
    host: str,
    port: int,
    community: str,
    snmp_version: SnmpVersion,
    enterprise_subid: int,
    varbinds: list[tuple[str, object]] | None,
    v3: V3Credentials | None = None,
) -> bool:
    return await _send_notification_async(
        trap_type,
        host,
        port,
        community,
        snmp_version,
        enterprise_subid,
        varbinds,
        "trap",
        v3=v3,
    )


def send_trap(
    trap_type: TrapType,
    host: str,
    port: int = 162,
    community: str = "public",
    snmp_version: SnmpVersion = "v2c",
    enterprise_subid: int = 0,
    varbinds: list[tuple[str, object]] | None = None,
    v3_user: str | None = None,
    v3_auth_key: str | None = None,
    v3_priv_key: str | None = None,
    v3_auth_proto: str = "md5",
    v3_priv_proto: str = "des",
) -> bool:
    """Send one SNMP trap (v1/v2c/v3). Returns True on success."""
    v3 = None
    if snmp_version == "v3" or v3_user:
        v3 = V3Credentials(v3_user or "", v3_auth_key, v3_priv_key, v3_auth_proto, v3_priv_proto)
        snmp_version = "v3"
    return asyncio.run(
        _send_trap_async(
            trap_type, host, port, community, snmp_version, enterprise_subid, varbinds, v3
        )
    )


def send_inform(
    trap_type: TrapType,
    host: str,
    port: int = 162,
    community: str = "public",
    snmp_version: SnmpVersion = "v2c",
    enterprise_subid: int = 0,
    varbinds: list[tuple[str, object]] | None = None,
    v3_user: str | None = None,
    v3_auth_key: str | None = None,
    v3_priv_key: str | None = None,
    v3_auth_proto: str = "md5",
    v3_priv_proto: str = "des",
) -> bool:
    """Send one SNMP inform (v2c/v3, manager must respond). Returns True on success."""
    v3 = None
    if snmp_version == "v3" or v3_user:
        v3 = V3Credentials(v3_user or "", v3_auth_key, v3_priv_key, v3_auth_proto, v3_priv_proto)
        snmp_version = "v3"
    return asyncio.run(
        _send_notification_async(
            trap_type,
            host,
            port,
            community,
            snmp_version,
            enterprise_subid,
            varbinds,
            "inform",
            v3=v3,
        )
    )


def default_enterprise_varbinds() -> list[tuple[str, object]]:
    """SIM-DATA: NTCIP event-style varbinds (docs/DEFAULT_DATA.md)."""
    return [
        ("1.3.6.1.4.1.1206.4.2.6.4.4.1.1", rfc1902.Integer32(1)),
        ("1.3.6.1.4.1.1206.4.2.6.4.4.1.2", rfc1902.Integer32(1)),
        ("1.3.6.1.4.1.1206.4.2.6.4.4.1.4", rfc1902.Counter32(1000)),
    ]
