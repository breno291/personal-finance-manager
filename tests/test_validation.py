import pytest

from app.services.validation import *
from app.config import CASH, CREDIT


# ==================================================
# VALIDATE REQUIRED STRING
# ==================================================

def test_validate_required_string():
    validate_required_string("Breno", "description")

    with pytest.raises(ValueError):
        validate_required_string("  ", "description")

    with pytest.raises(ValueError):
        validate_required_string(None, "description")

    with pytest.raises(ValueError):
        validate_required_string(123, "description")


# ==================================================
# VALIDATE POSITIVE INTEGER
# ==================================================

def test_validate_positive_integer():
    with pytest.raises(ValueError):
        validate_positive_integer("2", "Teste")

    with pytest.raises(ValueError):
        validate_positive_integer(True, "Teste")

    with pytest.raises(ValueError):
        validate_positive_integer(None, "Teste")

    with pytest.raises(ValueError):
        validate_positive_integer(0, "Teste")

    with pytest.raises(ValueError):
        validate_positive_integer(-1, "Teste")


# ==================================================
# VALIDATE INTEGER RANGE
# ==================================================

def test_validate_integer_range():
    validate_integer_range(1, "value", 1, 31)
    validate_integer_range(15, "value", 1, 31)
    validate_integer_range(31, "value", 1, 31)


def test_validate_integer_range_outside_range():
    with pytest.raises(ValueError):
        validate_integer_range(0, "value", 1, 31)

    with pytest.raises(ValueError):
        validate_integer_range(32, "value", 1, 31)


def test_validate_integer_range_with_invalid_value():
    with pytest.raises(ValueError):
        validate_integer_range(None, "value", 1, 31)

    with pytest.raises(ValueError):
        validate_integer_range("15", "value", 1, 31)

    with pytest.raises(ValueError):
        validate_integer_range(True, "value", 1, 31)


# ==================================================
# VALIDATE PAYMENT DAYS
# ==================================================

def test_validate_payment_days():
    validate_payment_days(None, None)

    with pytest.raises(ValueError):
        validate_payment_days("25", 5)

    with pytest.raises(ValueError):
        validate_payment_days(25, "5")

    with pytest.raises(ValueError):
        validate_payment_days(0, 5)

    with pytest.raises(ValueError):
        validate_payment_days(25, 0)

    with pytest.raises(ValueError):
        validate_payment_days(-1, 5)

    with pytest.raises(ValueError):
        validate_payment_days(25, -1)

    with pytest.raises(ValueError):
        validate_payment_days(32, 5)

    with pytest.raises(ValueError):
        validate_payment_days(25, 32)

    with pytest.raises(ValueError):
        validate_payment_days(None, 5)

    with pytest.raises(ValueError):
        validate_payment_days(25, None)

    with pytest.raises(ValueError):
        validate_payment_days(17, 17)


# ==================================================
# VALIDATE CREDIT PAYMENT DAYS
# ==================================================

def test_validate_credit_payment_days():
    validate_credit_payment_days(CREDIT, 25, 5)


def test_validate_credit_payment_days_without_days():
    with pytest.raises(ValueError):
        validate_credit_payment_days(CREDIT, None, None)

    with pytest.raises(ValueError):
        validate_credit_payment_days(CREDIT, 25, None)

    with pytest.raises(ValueError):
        validate_credit_payment_days(CREDIT, None, 5)


def test_validate_credit_payment_days_with_cash():
    validate_credit_payment_days(CASH, None, None)
    validate_credit_payment_days(CASH, 25, 5)


# ==================================================
# VALIDATE AND CONVERT DATE
# ==================================================

def test_validate_and_convert_date():
    assert validate_and_convert_date("28/06/2026") == "2026-06-28"

    with pytest.raises(ValueError):
        validate_and_convert_date("  ")

    with pytest.raises(ValueError):
        validate_and_convert_date(None)

    with pytest.raises(ValueError):
        validate_and_convert_date(12323)

    with pytest.raises(ValueError):
        validate_and_convert_date("31/05")

    with pytest.raises(ValueError):
        validate_and_convert_date("31-05-2026")

    with pytest.raises(ValueError):
        validate_and_convert_date("35/05/2026")

    with pytest.raises(ValueError):
        validate_and_convert_date("31/02/2026")


# ==================================================
# VALIDATE TRANSACTION STATUS
# ==================================================

def test_validate_transaction_status():
    validate_transaction_status(0)
    validate_transaction_status(1)
    validate_transaction_status(2)

    with pytest.raises(ValueError):
        validate_transaction_status("1")

    with pytest.raises(ValueError):
        validate_transaction_status(True)

    with pytest.raises(ValueError):
        validate_transaction_status(None)

    with pytest.raises(ValueError):
        validate_transaction_status(-1)

    with pytest.raises(ValueError):
        validate_transaction_status(3)



