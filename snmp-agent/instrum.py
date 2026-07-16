"""SNMP instrumentation: Get / GetNext / GetBulk / Set on flat OID store."""
from __future__ import annotations

import bisect

from pysnmp.proto import rfc1902, rfc1905
from pysnmp.smi import error
from pysnmp.smi.instrum import AbstractMibInstrumController

from oid_registry import OidMeta
from sim_data.validate import validate_value


class FlatMibInstrum(AbstractMibInstrumController):
    """RFC3413 instrumentation for all agent-side SNMP operations."""

    def __init__(
        self,
        oid_values: dict[tuple[int, ...], object],
        registry: dict[tuple[int, ...], OidMeta] | None = None,
        write_communities: set[str] | None = None,
        write_v3_users: set[str] | None = None,
    ):
        self._values = oid_values
        self._registry = registry or {}
        self._sorted = sorted(oid_values.keys())
        self._write_communities = write_communities or {"public"}
        self._write_v3_users = write_v3_users or set()

    @staticmethod
    def _parse_oid(name) -> tuple[int, ...]:
        text = name.prettyPrint().lstrip(".")
        if not text:
            return ()
        return tuple(int(x) for x in text.split("."))

    def _first_under_prefix(self, key: tuple[int, ...]) -> tuple[int, ...] | None:
        idx = bisect.bisect_right(self._sorted, key)
        if idx >= len(self._sorted):
            return None
        next_oid = self._sorted[idx]
        if len(next_oid) > len(key) and next_oid[: len(key)] == key:
            return next_oid
        return None

    def _resolve_key(self, key: tuple[int, ...]) -> tuple[int, ...] | None:
        if key in self._values:
            return key
        scalar = key + (0,)
        if scalar in self._values:
            return scalar
        row1 = key + (1,)
        if row1 in self._values:
            return row1
        # MIB Browser often appends .0 to table columns (treating them like scalars)
        if key and key[-1] == 0:
            base = key[:-1]
            if base + (1,) in self._values:
                return base + (1,)
            under = self._first_under_prefix(base)
            if under:
                return under
        # Table column without row / dual-index: first instance under prefix
        under = self._first_under_prefix(key)
        if under:
            return under
        return None

    def _verify_write_access(self, resolved: tuple[int, ...], idx: int, acInfo) -> None:
        """Access control: registry ACCESS + optional community (unit tests).

        UDP requests pass pysnmp's ``__verifyAccess`` as *acFun*; this flat
        agent relies on ``oid_registry`` instead (same as ``readVars``).
        """
        if not acInfo or len(acInfo) < 2:
            return
        acFun, acCtx = acInfo[0], acInfo[1]
        if callable(acFun):
            return
        if isinstance(acFun, int):
            sec_name = acCtx
            if sec_name is None:
                return
            if isinstance(sec_name, bytes):
                sec_name = sec_name.decode("ascii", errors="replace")
            if acFun in (3, "3", "usm"):
                if not self._write_v3_users:
                    return
                if sec_name not in self._write_v3_users:
                    raise error.NoAccessError(idx=idx)
                return
            if sec_name not in self._write_communities:
                raise error.NoAccessError(idx=idx)

    def _can_write(self, acInfo) -> bool:
        """Legacy entry point; prefer _verify_write_access per varbind."""
        if not acInfo or len(acInfo) < 2:
            return True
        acFun, acCtx = acInfo[0], acInfo[1]
        if callable(acFun):
            return True
        sec_name = acCtx
        if sec_name is None:
            return True
        if isinstance(sec_name, bytes):
            sec_name = sec_name.decode("ascii", errors="replace")
        if acInfo[0] in (3, "3", "usm"):
            if not self._write_v3_users:
                return True
            return sec_name in self._write_v3_users
        return sec_name in self._write_communities

    def readVars(self, varBinds, acInfo=(None, None)):
        """SNMP Get."""
        result = []
        for name, _val in varBinds:
            key = self._parse_oid(name)
            resolved = self._resolve_key(key)
            if resolved is not None:
                # Return canonical instance OID (scalar .0, table row key, etc.)
                result.append((rfc1902.ObjectName(resolved), self._values[resolved]))
            else:
                result.append((name, rfc1905.noSuchObject))
        return result

    def readNextVars(self, varBinds, acInfo=(None, None)):
        """SNMP GetNext / GetBulk (Bulk uses repeated GetNext)."""
        result = []
        for name, _val in varBinds:
            key = self._parse_oid(name)
            idx = bisect.bisect_right(self._sorted, key)
            if idx >= len(self._sorted):
                raise error.EndOfMibViewError(idx=0)
            next_oid = self._sorted[idx]
            result.append((rfc1902.ObjectName(next_oid), self._values[next_oid]))
        return result

    def writeVars(self, varBinds, acInfo=(None, None)):
        """SNMP Set with MIB ACCESS and SYNTAX validation (in-memory only; scheme A)."""
        result = []
        for idx, (name, val) in enumerate(varBinds):
            key = self._parse_oid(name)
            resolved = self._resolve_key(key)
            if resolved is None:
                raise error.NoSuchNameError(idx=idx)

            meta = self._registry.get(resolved)
            if meta and not meta.is_writable:
                raise error.NotWritableError(idx=idx)

            self._verify_write_access(resolved, idx, acInfo)

            if meta:
                try:
                    validate_value(meta.syntax, val)
                except ValueError:
                    raise error.WrongValueError(idx=idx) from None

            self._values[resolved] = val
            result.append((rfc1902.ObjectName(resolved), val))
        return result
