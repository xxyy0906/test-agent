"""Tests for all SNMP agent operations (Get / GetNext / GetBulk / Set)."""
from __future__ import annotations

from pathlib import Path

import pytest
from pysnmp.proto import rfc1902
from pysnmp.smi import error

from instrum import FlatMibInstrum
from mib_loader import MibLoader

MIB_DIR = Path(__file__).resolve().parent.parent.parent / "mibs" / "mibs_old"


@pytest.fixture(scope="module")
def instrum():
    loader = MibLoader(MIB_DIR, dev_cap=4)
    vals = loader.load()
    return FlatMibInstrum(vals, registry=loader.oid_registry, write_communities={"public"})


def test_get_scalar(instrum):
    oid = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 1, 0)
    name, val = instrum.readVars([(rfc1902.ObjectName(oid), None)])[0]
    assert name.prettyPrint() == ".".join(str(x) for x in oid)
    assert val.prettyPrint() == "255"


def test_get_next(instrum):
    start = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 1, 0)
    name, val = instrum.readNextVars([(rfc1902.ObjectName(start), None)])[0]
    assert tuple(int(x) for x in name.prettyPrint().split(".")) > start
    assert val is not None


def test_get_bulk_chain(instrum):
    """GetBulk is implemented via repeated GetNext in pysnmp BulkCommandResponder."""
    start = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 1, 0)
    current = start
    seen = []
    for _ in range(5):
        name, val = instrum.readNextVars([(rfc1902.ObjectName(current), None)])[0]
        oid = tuple(int(x) for x in name.prettyPrint().split("."))
        seen.append(oid)
        current = oid
    assert len(seen) == len(set(seen))
    assert all(b > a for a, b in zip(seen, seen[1:]))


def test_set_read_write_and_read_back(instrum):
    """Writable column: phasePedestrianClear (read-write)."""
    oid = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 3, 1)
    new_val = rfc1902.Integer32(100)
    name, val = instrum.writeVars(
        [(rfc1902.ObjectName(oid), new_val)],
        acInfo=(1, "public"),
    )[0]
    assert name.prettyPrint() == ".".join(str(x) for x in oid)
    assert val.prettyPrint() == "100"
    got = instrum.readVars([(rfc1902.ObjectName(oid), None)])[0][1]
    assert got.prettyPrint() == "100"


def test_set_read_only_rejected(instrum):
    """Read-only scalar maxPhases cannot be Set."""
    oid = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 1, 0)
    with pytest.raises(error.NotWritableError):
        instrum.writeVars(
            [(rfc1902.ObjectName(oid), rfc1902.Integer32(10))],
            acInfo=(1, "public"),
        )


def test_set_out_of_range_rejected(instrum):
    oid = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 3, 1)
    with pytest.raises(error.WrongValueError):
        instrum.writeVars(
            [(rfc1902.ObjectName(oid), rfc1902.Integer32(999))],
            acInfo=(1, "public"),
        )


def test_set_read_only_community_rejected():
    loader = MibLoader(MIB_DIR, dev_cap=4)
    inst = FlatMibInstrum(
        loader.load(),
        registry=loader.oid_registry,
        write_communities={"public"},
    )
    oid = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 3, 1)
    with pytest.raises(error.NoAccessError):
        inst.writeVars(
            [(rfc1902.ObjectName(oid), rfc1902.Integer32(50))],
            acInfo=(1, "readonly"),
        )


def test_set_no_such_object(instrum):
    bad = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 99, 99, 99)
    with pytest.raises(error.NoSuchNameError):
        instrum.writeVars([(rfc1902.ObjectName(bad), rfc1902.Integer32(1))])
