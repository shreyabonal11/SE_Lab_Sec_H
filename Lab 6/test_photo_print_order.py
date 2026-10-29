
import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


# Tests for extra_print_charge()

def test_unknown_print_size():
    with pytest.raises(ValueError, match="unknown print size"):
        extra_print_charge("A4", 10, "matte", False)


def test_negative_copies():
    with pytest.raises(ValueError, match="invalid copies"):
        extra_print_charge("4x6", -1, "matte", False)


def test_copies_within_included_limit():
    assert extra_print_charge("4x6", 15, "matte", False) == 0


def test_copies_exactly_at_included_limit():
    assert extra_print_charge("4x6", 20, "matte", False) == 0


def test_member_extra_included_prints():
    assert extra_print_charge("4x6", 25, "matte", True) == 0


def test_member_8x10_gets_no_extra_included_prints():
    assert extra_print_charge("8x10", 11, "matte", True) == 4


def test_extra_prints_matte_finish():
    assert extra_print_charge("4x6", 21, "matte", False) == 4


def test_extra_prints_non_matte_finish():
    assert extra_print_charge("4x6", 21, "glossy", False) == 7


def test_more_than_50_extra_prints_matte():
    assert extra_print_charge("4x6", 71, "matte", False) == 306


def test_more_than_50_extra_prints_canvas():
    assert extra_print_charge("4x6", 71, "canvas", False) == 714


def test_more_than_50_extra_prints_non_canvas():
    assert extra_print_charge("4x6", 71, "glossy", False) == 459


# Tests for order_valid()

def test_rush_order_within_limit():
    assert order_valid(10, 50, True) is True


def test_rush_order_exceeds_limit():
    assert order_valid(10, 51, True) is False


def test_non_rush_order_file_too_large():
    assert order_valid(26, 100, False) is False


def test_non_rush_order_at_file_size_limit():
    assert order_valid(25, 100, False) is True


def test_non_rush_order_at_copy_limit():
    assert order_valid(10, 500, False) is True


def test_non_rush_order_exceeds_copy_limit():
    assert order_valid(10, 501, False) is False


# Tests for dispatch_status()

def test_framed_order_on_time():
    assert dispatch_status(24, True, False) == "on_time"


def test_unframed_order_on_time():
    assert dispatch_status(12, False, False) == "on_time"


def test_international_order_on_time():
    assert dispatch_status(36, False, True) == "on_time"


def test_framed_international_order_on_time():
    assert dispatch_status(48, True, True) == "on_time"


def test_dispatch_tight_at_cutoff_minus_6():
    assert dispatch_status(18, True, False) == "tight"


def test_dispatch_tight_for_unframed_order():
    assert dispatch_status(6, False, False) == "tight"


def test_dispatch_missed():
    assert dispatch_status(5, False, False) == "missed"


def test_international_dispatch_missed():
    assert dispatch_status(29, False, True) == "missed"
