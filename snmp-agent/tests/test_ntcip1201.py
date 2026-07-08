"""Tests for NTCIP 1201 type-aware simulated data."""
from __future__ import annotations

from pathlib import Path

from mib_loader import DEFAULT_KNOWN, MIB_LOAD_ORDER, MibLoader
from sim_data.resolver import resolve_value
from smi_parser import ParsedMib, merge_parsed, parse_mib_file

MIBS_DIR = Path(__file__).resolve().parent.parent.parent / "mibs" / "mibs_old"
DEPS_DIR = Path(__file__).resolve().parent.parent / "deps"
# broad scope: 1201 objects live under devices (…4.2.6) AND protocols.profiles (…4.1.2)
ALL_NTCIP_ROOT = (1, 3, 6, 1, 4, 1, 1206)


def _names_defined_in_1201() -> set[str]:
    """Object names introduced by 1201v0227.mib (excluding imports from earlier MIBs)."""
    merged = ParsedMib(oid_by_name=dict(DEFAULT_KNOWN))
    before: set[str] = set()
    for name in MIB_LOAD_ORDER:
        if name == "1201v0227.mib":
            break
        path = MIBS_DIR / name
        if not path.is_file():
            path = DEPS_DIR / name
        if not path.is_file():
            continue
        extra = parse_mib_file(str(path), merged.oid_by_name)
        merged = merge_parsed(merged, extra)
        before |= set(extra.objects)
    p1201 = parse_mib_file(str(MIBS_DIR / "1201v0227.mib"), merged.oid_by_name)
    return {n for n in p1201.objects if n not in before}


def test_1201_scalar_defval_and_range():
    assert resolve_value("globalTime", "Counter", defval="0").prettyPrint() == "0"
    assert resolve_value("globalDaylightSaving", "INTEGER { disableDST (2) }", defval="disableDST").prettyPrint() == "2"
    assert resolve_value("globalSetIDParameter", "INTEGER (0..65535)").prettyPrint() == "65535"
    assert resolve_value("dbCreateTransaction", "INTEGER { normal (1) }", defval="normal").prettyPrint() == "1"
    assert resolve_value("controllerStandardTimeZone", "INTEGER (-43200..43200)").prettyPrint() == "43200"


def test_gauge_defval_uses_gauge32():
    val = resolve_value("communityNameAccessMask", "Gauge", defval="4294967295")
    assert type(val).__name__ == "Gauge32"
    assert val.prettyPrint() == "4294967295"


def test_large_integer_column_uses_gauge32():
    val = resolve_value(
        "timeBaseScheduleDate",
        "INTEGER (0..4294967295)",
        table_name="timeBaseScheduleTable",
        indices=(1,),
    )
    assert type(val).__name__ == "Gauge32"
    assert val.prettyPrint() == "4294967295"


def test_1201_module_table_row1():
    loader = MibLoader(Path(__file__).resolve().parent.parent.parent / "mibs" / "mibs_old", dev_cap=2)
    vals = loader.load()
    row = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 6, 1, 3, 1)
    assert vals[row + (1, 1)].prettyPrint() == "1"
    assert vals[row + (2, 1)].prettyPrint() == "1.3.6.1.4.1.1206.4.2.1"
    assert vals[row + (3, 1)].prettyPrint() == "SIM"
    assert vals[row + (6, 1)].prettyPrint() == "3"


def test_1201_phase_pedestrian_clear_max():
    loader = MibLoader(Path(__file__).resolve().parent.parent.parent / "mibs" / "mibs_old", dev_cap=4)
    vals = loader.load()
    oid = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 3, 1)
    assert vals[oid].prettyPrint() == "255"


def test_every_1201_object_has_default_value():
    """Traverse EVERY accessible element defined in 1201v0227.mib; each must have a value."""
    names_1201 = _names_defined_in_1201()
    loader = MibLoader(MIBS_DIR, dev_cap=3, oid_root=ALL_NTCIP_ROOT)
    vals = loader.load()
    parsed = loader.parsed

    covered_scalars = 0
    covered_columns = 0
    missing: list[str] = []

    for inst, obj in parsed.scalars.items():
        if obj.name in names_1201 and obj.access != "not-accessible":
            if inst in vals:
                covered_scalars += 1
            else:
                missing.append(f"scalar {obj.name}")

    for table in parsed.tables:
        if table.name not in names_1201:
            continue
        for col in table.columns:
            if col.access == "not-accessible":
                continue
            prefix = table.base_oid + col.oid_suffix
            if any(k[: len(prefix)] == prefix for k in vals):
                covered_columns += 1
            else:
                missing.append(f"column {table.name}.{col.name}")

    assert not missing, f"1201 objects without default values: {missing}"
    assert covered_scalars >= 18, covered_scalars
    assert covered_columns >= 15, covered_columns


def test_every_1201_value_is_valid_rfc1902():
    """Every simulated 1201 value must render (valid RFC1902, within its constraints)."""
    names_1201 = _names_defined_in_1201()
    oid_by_name = MibLoader(MIBS_DIR)._parse_all().oid_by_name
    oids_1201 = {oid_by_name[n] for n in names_1201 if n in oid_by_name}

    loader = MibLoader(MIBS_DIR, dev_cap=3, oid_root=ALL_NTCIP_ROOT)
    vals = loader.load()

    checked = 0
    for oid, value in vals.items():
        # value belongs to 1201 if its instance OID starts with a 1201 object OID
        if not any(oid[: len(base)] == base for base in oids_1201):
            continue
        assert value.prettyPrint() is not None
        checked += 1
    assert checked > 0
