"""Tests for Set alternate / invalid value generation."""
from __future__ import annotations

import pytest
from pysnmp.proto import rfc1902

from sim_data.set_values import alternate_set_value, invalid_set_value
from sim_data.validate import validate_value


def test_alternate_integer_range():
    cur = rfc1902.Integer32(255)
    new = alternate_set_value("INTEGER (0..255)", cur)
    validate_value("INTEGER (0..255)", new)
    assert new.prettyPrint() != "255"


def test_alternate_enum():
    cur = rfc1902.Integer32(2)
    new = alternate_set_value("INTEGER { disable(1), enable (2) }", cur)
    assert new.prettyPrint() == "1"


def test_alternate_octet():
    cur = rfc1902.OctetString(b"ZZZ")
    new = alternate_set_value('OCTET STRING (SIZE (2..12))', cur)
    validate_value('OCTET STRING (SIZE (2..12))', new)
    assert bytes(new) != bytes(cur)


def test_alternate_large_integer_gauge():
    cur = rfc1902.Gauge32(65535)
    new = alternate_set_value("INTEGER (0..65535)", cur)
    validate_value("INTEGER (0..65535)", new)
    assert new.prettyPrint() == "0"


def test_invalid_large_range():
    cur = rfc1902.Gauge32(4294967295)
    bad = invalid_set_value("INTEGER (0..4294967295)", cur)
    with pytest.raises(ValueError):
        validate_value("INTEGER (0..4294967295)", bad)


def test_invalid_unconstrained_integer():
    cur = rfc1902.Integer32(0)
    bad = invalid_set_value("INTEGER", cur)
    with pytest.raises(ValueError):
        validate_value("INTEGER", bad)


def test_invalid_enum():
    bad = invalid_set_value("INTEGER { other (1), dwell (2) }", rfc1902.Integer32(1))
    with pytest.raises(ValueError):
        validate_value("INTEGER { other (1), dwell (2) }", bad)
