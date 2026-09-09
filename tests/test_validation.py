import pytest

from app.services.validation import *


def test_validate_required_string():
    validate_required_string("Breno", "description")

    with pytest.raises(ValueError):
        validate_required_string("  ", "description")

    with pytest.raises(ValueError):
        validate_required_string(None, "description")

    with pytest.raises(ValueError):
        validate_required_string(123, "description")


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





