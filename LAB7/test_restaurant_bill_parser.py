from hypothesis import given, strategies as st
import pytest

from restaurant_bill_parser import (
    clean_dish_name,
    parse_item_prices,
    split_amount,
)


@given(st.text() | st.none())
def test_clean_dish_name_no_crash(value):
    try:
        clean_dish_name(value)
    except Exception as error:
        pytest.fail(f"clean_dish_name crashed for {value!r}: {error}")


@given(st.text() | st.none())
def test_parse_item_prices_no_crash(value):
    try:
        parse_item_prices(value)
    except Exception as error:
        pytest.fail(f"parse_item_prices crashed for {value!r}: {error}")


@given(st.text() | st.none())
def test_split_amount_no_crash(value):
    try:
        split_amount(value)
    except Exception as error:
        pytest.fail(f"split_amount crashed for {value!r}: {error}")