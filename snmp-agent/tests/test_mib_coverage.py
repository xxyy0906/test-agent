"""Coverage and type/range validation for 1201 and 1202 simulated data."""
from __future__ import annotations

from pathlib import Path

from mib_loader import DEFAULT_KNOWN, MIB_LOAD_ORDER, MibLoader
from sim_data.mib_syntax import load_full_syntax_map
from sim_data.validate import validate_value
from smi_parser import ParsedMib, merge_parsed, parse_mib_file

MIBS_DIR = Path(__file__).resolve().parent.parent.parent / "mibs" / "mibs_old"
DEPS_DIR = Path(__file__).resolve().parent.parent / "deps"
ALL_NTCIP_ROOT = (1, 3, 6, 1, 4, 1, 1206)
DEVICES_ROOT = (1, 3, 6, 1, 4, 1, 1206, 4, 2)


def _names_from_mib(mib_file: str) -> set[str]:
    merged = ParsedMib(oid_by_name=dict(DEFAULT_KNOWN))
    before: set[str] = set()
    for name in MIB_LOAD_ORDER:
        if name == mib_file:
            break
        path = MIBS_DIR / name
        if not path.is_file():
            path = DEPS_DIR / name
        if not path.is_file():
            continue
        extra = parse_mib_file(str(path), merged.oid_by_name)
        merged = merge_parsed(merged, extra)
        before |= set(extra.objects)
    parsed = parse_mib_file(str(MIBS_DIR / mib_file), merged.oid_by_name)
    return {n for n in parsed.objects if n not in before}


def _assert_mib_coverage(mib_file: str, oid_root: tuple[int, ...]):
    names = _names_from_mib(mib_file)
    loader = MibLoader(MIBS_DIR, dev_cap=3, oid_root=oid_root)
    vals = loader.load()
    parsed = loader.parsed
    missing: list[str] = []

    for inst, obj in parsed.scalars.items():
        if obj.name in names and obj.access != "not-accessible":
            if inst not in vals:
                missing.append(f"scalar {obj.name}")

    for table in parsed.tables:
        if table.name not in names:
            continue
        for col in table.columns:
            if col.access == "not-accessible":
                continue
            prefix = table.base_oid + col.oid_suffix
            if not any(k[: len(prefix)] == prefix for k in vals):
                missing.append(f"column {table.name}.{col.name}")

    assert not missing, f"{mib_file} missing defaults: {missing[:20]}"


def _assert_mib_values_valid(mib_file: str, oid_root: tuple[int, ...]):
    names = _names_from_mib(mib_file)
    full_syntax = load_full_syntax_map(MIBS_DIR, DEPS_DIR)
    loader = MibLoader(MIBS_DIR, dev_cap=3, oid_root=oid_root)
    vals = loader.load()
    parsed = loader.parsed

    obj_by_name = parsed.objects
    errors: list[str] = []

    for oid, value in vals.items():
        matched = None
        for inst, obj in parsed.scalars.items():
            if inst == oid and obj.name in names:
                matched = obj.name
                break
        if not matched:
            for table in parsed.tables:
                if table.name not in names:
                    continue
                for col in table.columns:
                    prefix = table.base_oid + col.oid_suffix
                    if oid[: len(prefix)] == prefix:
                        matched = col.name
                        break
                if matched:
                    break
        if not matched or matched not in full_syntax:
            continue
        try:
            validate_value(full_syntax[matched], value)
        except ValueError as exc:
            errors.append(f"{matched} ({oid}): {exc}")

    assert not errors, f"{mib_file} invalid values:\n" + "\n".join(errors[:15])


def test_1201_full_coverage():
    _assert_mib_coverage("1201v0227.mib", ALL_NTCIP_ROOT)


def test_1201_values_in_range():
    _assert_mib_values_valid("1201v0227.mib", ALL_NTCIP_ROOT)


def test_1202_full_coverage():
    _assert_mib_coverage("1202v0218.mib", DEVICES_ROOT)


def test_1202_values_in_range():
    _assert_mib_values_valid("1202v0218.mib", DEVICES_ROOT)


def test_1202_preempt_defval():
    loader = MibLoader(MIBS_DIR, dev_cap=2, oid_root=DEVICES_ROOT)
    vals = loader.load()
    # preemptControl DEFVAL { 0 }
    oid = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 6, 2, 1, 2, 1)
    assert vals[oid].prettyPrint() == "0"


def test_1202_split_mode_enum_max():
    from sim_data.mib_syntax import load_full_syntax_map
    from sim_data.resolver import resolve_value

    syn = load_full_syntax_map(MIBS_DIR, DEPS_DIR)["splitMode"]
    val = resolve_value("splitMode", syn)
    assert type(val).__name__ == "Integer32"
    assert int(val.prettyPrint()) > 1
