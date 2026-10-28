"""Lab 6 - Step 1: tests written to reach at least 90% LINE coverage."""
import pytest
from restaurant_bill import bill_total, split_bill, table_wait


# ---------- starter tests (given) ----------
def test_dine_in_bill():
    assert bill_total("dine_in", 1000, 2, False) == 1155


def test_even_split():
    assert split_bill(1000, 4, 10) == 275


# ---------- bill_total ----------
def test_takeaway_has_no_service_charge():
    # service 0 -> total 1000, plus 5% = 1050
    assert bill_total("takeaway", 1000, 2, False) == 1050


def test_rooftop_service_charge():
    # service 15% = 150 -> 1150, tax 1150*5//100 = 57 -> 1207
    assert bill_total("rooftop", 1000, 2, False) == 1207


def test_happy_hour_discount_on_dine_in():
    # food 1000 -> 800, service 80 -> 880, tax 44 -> 924
    assert bill_total("dine_in", 1000, 2, True) == 924


def test_large_group_adds_flat_service_fee():
    # service 100 + 200 flat = 300 -> 1300, tax 65 -> 1365
    assert bill_total("dine_in", 1000, 8, False) == 1365


def test_unknown_section_rejected():
    with pytest.raises(ValueError, match="unknown section"):
        bill_total("balcony", 500, 2, False)


def test_negative_food_total_rejected():
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", -1, 2, False)


# ---------- split_bill ----------
def test_uneven_split_rounds_up():
    # 1000 / 3 = 333.33 -> each person pays 334
    assert split_bill(1000, 3, 0) == 334


def test_split_with_zero_people_rejected():
    with pytest.raises(ValueError, match="invalid people count"):
        split_bill(1000, 0, 10)


# ---------- table_wait ----------
def test_party_over_twelve_must_call_ahead():
    assert table_wait(13, 5, False) == "call ahead"


def test_reservation_is_seated_immediately():
    assert table_wait(4, 0, True) == "seat now"


def test_no_free_tables_means_waitlist():
    assert table_wait(2, 0, False) == "waitlist"


def test_large_party_with_one_free_table_waits():
    assert table_wait(8, 1, False) == "waitlist"
