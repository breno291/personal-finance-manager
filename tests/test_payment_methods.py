import pytest
from app.database.payment_methods import *

def test_insert_payment_method(connection):
    payment_method_id = insert_payment_method(connection, "Nubank", 2, 25, 5)
    assert payment_method_id is not None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM payment_methods WHERE id = ?", (payment_method_id,))
    payment = cursor.fetchone()

    assert payment[0] == payment_method_id # "id
    assert payment[1] == "Nubank" # description
    assert payment[2] == 2 # payment_type
    assert payment[3] == 25 # closing_day
    assert payment[4] == 5 # due_day
    assert payment[5] == 0 # removed


def test_insert_payment_method_without_description(connection):
    with pytest.raises(ValueError):
        insert_payment_method(connection, "  ", 2, 25, 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, None, 2, 25, 5)
    with pytest.raises(ValueError):
        insert_payment_method(connection, 123, 2, 25, 5)


def test_insert_payment_method_with_invalid_payment_type(connection):
    with pytest.raises(ValueError):
        insert_payment_method(connection, "PicPay", "2", 25, 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "PicPay", True, 25, 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "PicPay", None, 25, 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "PicPay", 0, 25, 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "PicPay", -1, 25, 5)


def test_insert_payment_method_with_invalid_days(connection):
    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", 2, "25", 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", 2, 25, "5")

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", 2, 0, 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", 2, 25, 0)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", 2, -1, 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", 2, 25, -1)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", 2, 32, 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", 2, 25, 32)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", 2, None, 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", 2, 25, None)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", 2, 17, 17)


def test_insert_payment_method_with_null_days(connection):
    payment_method_id = insert_payment_method(connection, "Nubank", 2, None, None)
    assert payment_method_id is not None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM payment_methods WHERE id = ?", (payment_method_id,))
    payment = cursor.fetchone()

    assert payment[0] == payment_method_id # "id
    assert payment[1] == "Nubank" # description
    assert payment[2] == 2 # payment_type
    assert payment[3] is None # closing_day
    assert payment[4] is None # due_day
    assert payment[5] == 0 # removed


def test_select_payment_method_by_id(connection):
    payment_method_id = insert_payment_method(connection, "Santander", 2, 26, 4)

    payment_method = select_payment_method_by_id(connection, payment_method_id)

    assert payment_method[0] == payment_method_id # "id
    assert payment_method[1] == "Santander" # description
    assert payment_method[2] == 2 # payment_type
    assert payment_method[3] == 26 # closing_day
    assert payment_method[4] == 4 # due_day
    assert payment_method[5] == 0 # removed


def test_select_payment_method_by_id_with_invalid_id(connection):
    with pytest.raises(ValueError):
        select_payment_method_by_id(connection, -1)

    with pytest.raises(ValueError):
        select_payment_method_by_id(connection, 0)

    with pytest.raises(ValueError):
        select_payment_method_by_id(connection, None)

    with pytest.raises(ValueError):
        select_payment_method_by_id(connection, "1")

    with pytest.raises(ValueError):
        select_payment_method_by_id(connection, False)


def test_select_payment_method_by_id_with_nonexistent_id(connection):
    assert select_payment_method_by_id(connection, 3) is None




