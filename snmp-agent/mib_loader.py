"""Load NTCIP MIBs from mibs_old and build flat OID value store."""
from __future__ import annotations

from pathlib import Path

from oid_utils import DEVICES_OID_ROOT, ASC_OID_ROOT, GLOBAL_OID_ROOT, oid_dotted, under_prefix
from oid_registry import build_oid_registry
from sim_data.loader import apply_overrides
from sim_data.mib_syntax import load_full_syntax_map
from sim_data.resolver import resolve_value
from smi_parser import ParsedMib, merge_parsed, parse_mib_file
from table_expander import expand_table

DEFAULT_KNOWN = {
    "ccitt": (0,),
    "null": (0, 0),
    "iso": (1,),
    "org": (1, 3),
    "dod": (1, 3, 6),
    "internet": (1, 3, 6, 1),
    "directory": (1, 3, 6, 1, 1),
    "mgmt": (1, 3, 6, 1, 2),
    "experimental": (1, 3, 6, 1, 3),
    "private": (1, 3, 6, 1, 4),
    "enterprises": (1, 3, 6, 1, 4, 1),
}

MIB_LOAD_ORDER = [
    "Rfc1155.smi",
    "rfc1212.smi",
    "rfc1158.smi",
    "RFC1213-MIB.mib",
    "8004v0134.mib",
    "1103v0125.mib",
    "1201v0227.mib",
    "1202v0218.mib",
]

MAX_SCALAR_NAMES = (
    "globalMaxModules",
    "maxTimeBaseScheduleEntries",
    "maxDayPlans",
    "maxDayPlanEvents",
    "maxGroupAddresses",
    "maxEventClasses",
    "maxEventLogConfigs",
    "maxEventLogSize",
    "communityNamesMax",
    "maxPhases",
    "maxPhaseGroups",
    "maxVehicleDetectors",
    "maxVehicleDetectorStatusGroups",
    "maxPedestrianDetectors",
    "maxAlarmGroups",
    "maxSpecialFunctionOutputs",
    "maxPatterns",
    "maxSplits",
    "maxTimebaseAscActions",
    "maxPreempts",
    "maxRings",
    "maxSequences",
    "maxRingControlGroups",
    "maxChannels",
    "maxChannelStatusGroups",
    "maxOverlaps",
    "maxOverlapStatusGroups",
    "maxPort1Addresses",
    "auxIOTableNumDigitalPorts",
    "auxIOTableNumAnalogPorts",
    "numFonts",
)


class MibLoader:
    def __init__(
        self,
        mib_dir: str | Path,
        deps_dir: str | Path | None = None,
        default_data_path: str | Path | None = None,
        dev_cap: int | None = None,
        oid_root: tuple[int, ...] | None = DEVICES_OID_ROOT,
    ):
        self.mib_dir = Path(mib_dir)
        self.deps_dir = Path(deps_dir) if deps_dir else Path(__file__).resolve().parent / "deps"
        self.default_data_path = Path(default_data_path) if default_data_path else None
        self.dev_cap = dev_cap
        self.oid_root = oid_root
        self.parsed: ParsedMib | None = None
        self.stats: dict[str, int] = {}
        self.oid_registry: dict = {}
        self.syntax_by_name: dict[str, str] = {}

    def load(self) -> dict[tuple[int, ...], object]:
        parsed = self._parse_all()
        self.parsed = parsed
        values: dict[tuple[int, ...], object] = {}
        full_syntax = load_full_syntax_map(self.mib_dir, self.deps_dir)
        syntax_by_name = {
            o.name: full_syntax.get(o.name, o.syntax) for o in parsed.objects.values()
        }
        scalar_values: dict[str, int] = {}

        for inst, obj in parsed.scalars.items():
            if obj.access == "not-accessible":
                continue
            if not under_prefix(obj.oid, self.oid_root):
                continue
            syn = syntax_by_name.get(obj.name, obj.syntax)
            val = resolve_value(obj.name, syn, defval=obj.defval or None)
            values[inst] = val
            if (
                obj.name.startswith("max")
                or obj.name.startswith("globalMax")
                or obj.name.startswith("auxIOTableNum")
                or obj.name == "numFonts"
            ):
                try:
                    scalar_values[obj.name] = int(val.prettyPrint())
                except (AttributeError, ValueError, TypeError):
                    pass

        self._sync_max_scalars(scalar_values, syntax_by_name, parsed)

        for table in parsed.tables:
            if not under_prefix(table.base_oid, self.oid_root):
                continue
            expand_table(table, scalar_values, syntax_by_name, values, self.dev_cap)

        if self.default_data_path and self.default_data_path.is_file():
            apply_overrides(values, self.default_data_path, parsed.oid_by_name, syntax_by_name)

        self.syntax_by_name = syntax_by_name
        self.oid_registry = build_oid_registry(parsed, values, syntax_by_name)

        self.stats = {
            "total": len(values),
            "devices": sum(1 for k in values if under_prefix(k, DEVICES_OID_ROOT)),
            "asc": sum(1 for k in values if under_prefix(k, ASC_OID_ROOT)),
            "global": sum(1 for k in values if under_prefix(k, GLOBAL_OID_ROOT)),
        }
        return values

    def _parse_all(self) -> ParsedMib:
        merged = ParsedMib(oid_by_name=dict(DEFAULT_KNOWN))
        for name in MIB_LOAD_ORDER:
            if name.endswith(".mib") and (self.mib_dir / name).is_file():
                path = self.mib_dir / name
            elif (self.deps_dir / name).is_file():
                path = self.deps_dir / name
            elif (self.mib_dir / name).is_file():
                path = self.mib_dir / name
            else:
                continue
            extra = parse_mib_file(str(path), merged.oid_by_name)
            merged = merge_parsed(merged, extra)
        return merged

    @staticmethod
    def _sync_max_scalars(
        scalar_values: dict[str, int],
        syntax_by_name: dict[str, str],
        parsed: ParsedMib,
    ) -> None:
        for name in MAX_SCALAR_NAMES:
            if name in scalar_values:
                continue
            if name in syntax_by_name:
                obj = parsed.objects.get(name)
                if obj:
                    val = resolve_value(name, syntax_by_name.get(name, obj.syntax), defval=obj.defval or None)
                else:
                    from value_factory import max_value_for_syntax

                    val = max_value_for_syntax(syntax_by_name[name])
                try:
                    scalar_values[name] = int(val.prettyPrint())
                except (AttributeError, ValueError, TypeError):
                    scalar_values[name] = 255
