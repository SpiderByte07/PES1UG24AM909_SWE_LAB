"""Lab 6 - Step 2: tests written to reach at least 90% BRANCH coverage.

Includes every test from the code-coverage file, plus tests that make each
decision (if / elif / and / or) go both True and False, including boundaries.
"""
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


def test_zero_guests_rejected():
    # second half of "food_total < 0 or guests < 1"
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", 100, 0, False)


def test_boundary_zero_food_and_one_guest_is_valid():
    assert bill_total("dine_in", 0, 1, False) == 0


def test_happy_hour_does_not_apply_to_takeaway():
    # "is_happy_hour and section != takeaway" -> True and False
    assert bill_total("takeaway", 1000, 2, True) == 1050


def test_party_of_seven_gets_no_flat_fee():
    # boundary just below "guests >= 8"
    assert bill_total("dine_in", 1000, 7, False) == 1155


def test_integer_division_rounds_down():
    # service 105*10//100 = 10 -> 115, tax 115*5//100 = 5 -> 120
    assert bill_total("dine_in", 105, 2, False) == 120


# ---------- split_bill ----------
def test_uneven_split_rounds_up():
    # 1000 / 3 = 333.33 -> each person pays 334
    assert split_bill(1000, 3, 0) == 334


def test_split_with_zero_people_rejected():
    with pytest.raises(ValueError, match="invalid people count"):
        split_bill(1000, 0, 10)


def test_negative_tip_rejected():
    with pytest.raises(ValueError, match="invalid tip"):
        split_bill(1000, 2, -5)


def test_zero_tip_is_allowed():
    assert split_bill(1000, 2, 0) == 500


def test_single_person_pays_everything_with_tip():
    assert split_bill(1000, 1, 10) == 1100


# ---------- table_wait ----------
def test_party_over_twelve_must_call_ahead():
    assert table_wait(13, 5, False) == "call ahead"


def test_reservation_is_seated_immediately():
    assert table_wait(4, 0, True) == "seat now"


def test_no_free_tables_means_waitlist():
    assert table_wait(2, 0, False) == "waitlist"


def test_large_party_with_one_free_table_waits():
    assert table_wait(8, 1, False) == "waitlist"


def test_large_party_with_two_free_tables_is_seated():
    # "party_size > 6 and free_tables < 2" -> True and False
    assert table_wait(8, 2, False) == "seat now"


def test_party_of_six_with_one_free_table_is_seated():
    # boundary: party_size > 6 is False
    assert table_wait(6, 1, False) == "seat now"


def test_party_of_seven_with_one_free_table_waits():
    # boundary: party_size > 6 is True
    assert table_wait(7, 1, False) == "waitlist"


def test_small_party_with_free_tables_is_seated():
    # falls through every check to the default "seat now"
    assert table_wait(2, 5, False) == "seat now"


def test_party_of_twelve_with_reservation_is_seated():
    # boundary just below "party_size > 12"
    assert table_wait(12, 3, True) == "seat now"


def test_party_over_twelve_calls_ahead_even_with_reservation():
    assert table_wait(13, 5, True) == "call ahead"
