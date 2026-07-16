"""Shared Set / read-back test runner (in-process and result records)."""
from __future__ import annotations

from dataclasses import dataclass, field

from pysnmp.proto import rfc1902, rfc1905
from pysnmp.smi import error

from sim_data.set_values import SetTestCase, alternate_set_value, invalid_set_value
from sim_data.validate import validate_value


@dataclass
class SetTestResult:
    name: str
    instance_oid: str
    access: str
    syntax: str
    status: str  # PASS | FAIL | SKIP
    detail: str = ""
    old_value: str = ""
    new_value: str = ""
    phase: str = "set-readback"  # set-readback | reject-writable | reject-readonly


@dataclass
class SetTestSummary:
    results: list[SetTestResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.status == "PASS" for r in self.results)

    def counts(self) -> dict[str, int]:
        out = {"PASS": 0, "FAIL": 0, "SKIP": 0}
        for r in self.results:
            out[r.status] = out.get(r.status, 0) + 1
        return out


def _oid_str(oid: tuple[int, ...]) -> str:
    return ".".join(str(x) for x in oid)


def _pretty(val) -> str:
    if val is None:
        return ""
    t = type(val).__name__
    if t == "OctetString":
        raw = bytes(val)
        try:
            return repr(raw.decode("ascii"))
        except UnicodeDecodeError:
            return raw.hex()
    return val.prettyPrint()


def _snmp_error_name(exc: BaseException) -> str:
    return exc.__class__.__name__


def run_writable_set_readback(
    instrum,
    cases: list[SetTestCase],
) -> list[SetTestResult]:
    results: list[SetTestResult] = []
    for case in cases:
        oid_s = _oid_str(case.instance_oid)
        base = dict(
            name=case.name,
            instance_oid=oid_s,
            access=case.access,
            syntax=case.syntax[:80],
            phase="set-readback",
        )
        try:
            _, old_val = instrum.readVars([(rfc1902.ObjectName(case.instance_oid), None)])[0]
            if old_val.__class__.__name__ == "noSuchObject":
                results.append(SetTestResult(**base, status="FAIL", detail="Get: noSuchObject"))
                continue

            new_val = alternate_set_value(case.syntax, old_val)
            validate_value(case.syntax, new_val)

            resp_name, set_val = instrum.writeVars(
                [(rfc1902.ObjectName(case.instance_oid), new_val)],
                acInfo=(1, "public"),
            )[0]
            if resp_name.prettyPrint().lstrip(".") != oid_s:
                results.append(
                    SetTestResult(
                        **base,
                        status="FAIL",
                        detail=f"Set response OID mismatch: {resp_name.prettyPrint()}",
                        old_value=_pretty(old_val),
                        new_value=_pretty(set_val),
                    )
                )
                continue

            _, got = instrum.readVars([(rfc1902.ObjectName(case.instance_oid), None)])[0]
            if _pretty(got) != _pretty(set_val):
                results.append(
                    SetTestResult(
                        **base,
                        status="FAIL",
                        detail=f"read-back mismatch: got {_pretty(got)}",
                        old_value=_pretty(old_val),
                        new_value=_pretty(set_val),
                    )
                )
                continue

            bad = invalid_set_value(case.syntax, got)
            try:
                instrum.writeVars(
                    [(rfc1902.ObjectName(case.instance_oid), bad)],
                    acInfo=(1, "public"),
                )
                results.append(
                    SetTestResult(
                        **base,
                        status="FAIL",
                        detail="invalid Set should have been rejected",
                        old_value=_pretty(old_val),
                        new_value=_pretty(got),
                    )
                )
            except error.WrongValueError:
                results.append(
                    SetTestResult(
                        **base,
                        status="PASS",
                        detail="invalid Set rejected",
                        old_value=_pretty(old_val),
                        new_value=_pretty(got),
                    )
                )
            except error.PySnmpError as exc:
                results.append(
                    SetTestResult(
                        **base,
                        status="PASS",
                        detail=f"invalid Set rejected ({_snmp_error_name(exc)})",
                        old_value=_pretty(old_val),
                        new_value=_pretty(got),
                    )
                )
        except error.PySnmpError as exc:
            results.append(SetTestResult(**base, status="FAIL", detail=_snmp_error_name(exc)))
        except ValueError as exc:
            results.append(SetTestResult(**base, status="FAIL", detail=str(exc)))
    return results


def run_readonly_reject(
    instrum,
    cases: list[SetTestCase],
) -> list[SetTestResult]:
    results: list[SetTestResult] = []
    for case in cases:
        oid_s = _oid_str(case.instance_oid)
        base = dict(
            name=case.name,
            instance_oid=oid_s,
            access=case.access,
            syntax=case.syntax[:80],
            phase="reject-readonly",
        )
        try:
            _, old_val = instrum.readVars([(rfc1902.ObjectName(case.instance_oid), None)])[0]
            if old_val.__class__.__name__ == "noSuchObject":
                results.append(SetTestResult(**base, status="SKIP", detail="noSuchObject"))
                continue
            new_val = alternate_set_value(case.syntax, old_val)
            instrum.writeVars(
                [(rfc1902.ObjectName(case.instance_oid), new_val)],
                acInfo=(1, "public"),
            )
            results.append(SetTestResult(**base, status="FAIL", detail="Set should be rejected"))
        except (error.NotWritableError, error.NoAccessError):
            results.append(SetTestResult(**base, status="PASS", detail="rejected"))
        except error.PySnmpError as exc:
            # noSuchName on index-only edge cases still counts as reject
            if exc.__class__.__name__ in ("NoSuchNameError", "NotWritableError"):
                results.append(SetTestResult(**base, status="PASS", detail=_snmp_error_name(exc)))
            else:
                results.append(SetTestResult(**base, status="FAIL", detail=_snmp_error_name(exc)))
    return results


def run_index_not_accessible_reject(instrum, oids: list[tuple[int, ...]]) -> list[SetTestResult]:
    results: list[SetTestResult] = []
    for oid in oids:
        oid_s = _oid_str(oid)
        base = dict(
            name="(index)",
            instance_oid=oid_s,
            access="not-accessible",
            syntax="",
            phase="reject-index",
        )
        try:
            instrum.writeVars(
                [(rfc1902.ObjectName(oid), rfc1902.Integer32(1))],
                acInfo=(1, "public"),
            )
            results.append(SetTestResult(**base, status="FAIL", detail="Set should be rejected"))
        except error.NotWritableError:
            results.append(SetTestResult(**base, status="PASS", detail="notWritable"))
        except error.PySnmpError as exc:
            results.append(
                SetTestResult(
                    **base,
                    status="PASS" if exc.__class__.__name__ == "NotWritableError" else "FAIL",
                    detail=_snmp_error_name(exc),
                )
            )
    return results
