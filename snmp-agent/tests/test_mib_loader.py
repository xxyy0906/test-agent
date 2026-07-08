"""Basic tests for NTCIP snmp-agent."""
from __future__ import annotations

from pathlib import Path

from mib_loader import MibLoader
from oid_utils import DEVICES_OID_ROOT
from smi_parser import parse_mib_file


ROOT = Path(__file__).resolve().parent.parent.parent
MIB_DIR = ROOT / "mibs" / "mibs_old"


def test_8004_parse():
    known = {"enterprises": (1, 3, 6, 1, 4, 1)}
    parsed = parse_mib_file(str(MIB_DIR / "8004v0134.mib"), known)
    assert "nema" in parsed.oid_by_name
    assert parsed.oid_by_name["nema"] == (1, 3, 6, 1, 4, 1, 1206)


def test_loader_devices_scope():
    loader = MibLoader(MIB_DIR, dev_cap=4, oid_root=DEVICES_OID_ROOT)
    vals = loader.load()
    assert len(vals) > 500
    assert all(k[: len(DEVICES_OID_ROOT)] == DEVICES_OID_ROOT for k in vals)
    assert (1, 3, 6, 1, 4, 1, 1206, 4, 2, 6, 1, 1, 0) in vals


def test_every_devices_object_has_default_value():
    """Every accessible object under devices (…4.2, incl. …4.2.1 ASC) gets a default value."""
    loader = MibLoader(MIB_DIR, dev_cap=3, oid_root=DEVICES_OID_ROOT)
    vals = loader.load()
    parsed = loader.parsed

    missing: list[str] = []
    for inst, obj in parsed.scalars.items():
        if inst[: len(DEVICES_OID_ROOT)] != DEVICES_OID_ROOT:
            continue
        if obj.access == "not-accessible":
            continue
        if inst not in vals:
            missing.append(f"scalar {obj.name}")

    for table in parsed.tables:
        if table.base_oid[: len(DEVICES_OID_ROOT)] != DEVICES_OID_ROOT:
            continue
        for col in table.columns:
            if col.access == "not-accessible":
                continue
            prefix = table.base_oid + col.oid_suffix
            if not any(k[: len(prefix)] == prefix for k in vals):
                missing.append(f"column {table.name}.{col.name}")

    assert not missing, f"devices objects without default values: {missing}"


def test_every_value_renders():
    """No simulated value crashes on prettyPrint (all valid RFC1902 within constraints)."""
    loader = MibLoader(MIB_DIR, dev_cap=3, oid_root=DEVICES_OID_ROOT)
    vals = loader.load()
    for value in vals.values():
        assert value.prettyPrint() is not None
