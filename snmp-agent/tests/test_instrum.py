"""Tests for Get resolution and syntax max values."""
from __future__ import annotations

from pathlib import Path

from instrum import FlatMibInstrum
from mib_loader import MibLoader
from pysnmp.proto import rfc1902
from value_factory import max_value_for_syntax


def test_integer_range_uses_maximum():
    assert max_value_for_syntax("INTEGER (0..255)").prettyPrint() == "255"
    assert max_value_for_syntax("INTEGER (2..255)").prettyPrint() == "255"
    # INDEX column uses row number, not range max
    assert max_value_for_syntax("INTEGER (1..255)", index_value=3).prettyPrint() == "3"


def test_get_table_column_without_row_index():
    loader = MibLoader(Path(__file__).resolve().parent.parent.parent / "mibs" / "mibs_old", dev_cap=4)
    vals = loader.load()
    inst = FlatMibInstrum(vals)
    col_oid = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 3)
    row1 = col_oid + (1,)
    name = rfc1902.ObjectName(col_oid)
    result = inst.readVars([(name, None)])
    assert result[0][0].prettyPrint() == "1.3.6.1.4.1.1206.4.2.1.1.2.1.3.1"
    assert result[0][1].prettyPrint() == "255"


def test_get_table_column_fills_index_key():
    """Column OID without row index resolves to row 1 instance (table key)."""
    loader = MibLoader(Path(__file__).resolve().parent.parent.parent / "mibs" / "mibs_old", dev_cap=4)
    inst = FlatMibInstrum(loader.load())
    col = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 8, 2, 1, 1)  # channelNumber
    row1 = col + (1,)
    name, val = inst.readVars([(rfc1902.ObjectName(col), None)])[0]
    assert name.prettyPrint() == ".".join(str(x) for x in row1)
    assert val.prettyPrint() == "1"


def test_get_table_column_with_dot_zero():
    """MIB Browser often Get column OID with trailing .0."""
    loader = MibLoader(Path(__file__).resolve().parent.parent.parent / "mibs" / "mibs_old", dev_cap=4)
    inst = FlatMibInstrum(loader.load())
    col0 = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 3, 0)
    result = inst.readVars([(rfc1902.ObjectName(col0), None)])[0]
    assert result[1].prettyPrint() == "255"


def test_get_table_node_returns_first_row():
    """Double-click on phaseTable should return first table cell."""
    loader = MibLoader(Path(__file__).resolve().parent.parent.parent / "mibs" / "mibs_old", dev_cap=4)
    inst = FlatMibInstrum(loader.load())
    table = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2)
    result = inst.readVars([(rfc1902.ObjectName(table), None)])[0]
    assert result[1].prettyPrint() == "1"


def test_phase_red_revert_oid_and_value():
    """phaseRedRevert is column 1.10 (not 1.9); default = 255."""
    loader = MibLoader(Path(__file__).resolve().parent.parent.parent / "mibs" / "mibs_old", dev_cap=4)
    inst = FlatMibInstrum(loader.load())
    col = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 10)
    row1 = col + (1,)
    result = inst.readVars([(rfc1902.ObjectName(col), None)])
    assert result[0][0].prettyPrint() == ".".join(str(x) for x in row1)
    assert result[0][1].prettyPrint() == "255"
    # .9 is phaseRedClear, also 255
    clear = (1, 3, 6, 1, 4, 1, 1206, 4, 2, 1, 1, 2, 1, 9)
    r2 = inst.readVars([(rfc1902.ObjectName(clear), None)])
    assert r2[0][1].prettyPrint() == "255"
