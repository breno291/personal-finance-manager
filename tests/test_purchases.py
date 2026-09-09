import pytest
import sqlite3

from app.database.purchases import *
from app.database.payment_methods import insert_payment_method

def test_insert_purchase(connection):
    payment_method_id = insert_payment_method(connection, "Nubank", 2, 25, 5)
    purchase_id = insert_purchase(connection, "   Ração   ", "30/08/2026", 1550, 1, payment_method_id, 2, 10)

    assert purchase_id is not None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM purchases WHERE id = ?", (purchase_id,))
    purchase = cursor.fetchone()

    assert purchase[0] ==  purchase_id# id
    assert purchase[1] == "Ração" # description
    assert purchase[2] == "2026-08-30" # purchase_date
    assert purchase[3] == 1550 # value
    assert purchase[4] == 1 # installment_count
    assert purchase[5] == payment_method_id # payment_method_id
    assert purchase[6] == 2 # category_id
    assert purchase[7] == 10 # subcategory_id
    assert purchase[8] is not None # created_at
    assert purchase[9] is None # updated_at
    assert purchase[10] == 0 # removed


def test_insert_purchase_without_description(connection):
    payment_method_id = insert_payment_method(connection, "Nubank", 2, 25, 5)
    with pytest.raises(ValueError):
        insert_purchase(connection, "  ", "30/08/2026", 1550, 1, payment_method_id, 2, 10)

    with pytest.raises(ValueError):
        insert_purchase(connection, None, "30/08/2026", 1550, 1, payment_method_id, 2, 10)

    with pytest.raises(ValueError):
        insert_purchase(connection, 123, "30/08/2026", 1550, 1, payment_method_id, 2, 10)


def test_insert_purchase_invalid_purchase_date(connection):
    payment_method_id = insert_payment_method(connection, "Nubank", 2, 25, 5)

    with pytest.raises(ValueError):
        insert_purchase(connection, "Ração", " ", 1550, 1, payment_method_id, 2, 10)

    with pytest.raises(ValueError):
        insert_purchase(connection, "Ração", None, 1550, 1, payment_method_id, 2, 10)

    with pytest.raises(ValueError):
        insert_purchase(connection, "Ração", "30/09", 1550, 1, payment_method_id, 2, 10)

    with pytest.raises(ValueError):
        insert_purchase(connection, "Ração", 12323, 1550, 1, payment_method_id, 2, 10)

    with pytest.raises(ValueError):
        insert_purchase(connection, "Ração", "31-05-2026", 1550, 1, payment_method_id, 2, 10)

    with pytest.raises(ValueError):
        insert_purchase(connection, "Ração", "35/05/2026", 1550, 1, payment_method_id, 2, 10)

    with pytest.raises(ValueError):
        insert_purchase(connection, "Ração", "31/02/2026", 1550, 1, payment_method_id, 2, 10)


def test_insert_purchase_with_invalid_positive_integer(connection):
    payment_method_id = insert_payment_method(connection, "Nubank", 2, 25, 5)

    with pytest.raises(ValueError):
        insert_purchase(connection, "Ração", "31/05/2024", None, 1, payment_method_id, 2, 10)

    with pytest.raises(ValueError):
        insert_purchase(connection, "Ração", "31/05/2024", 12, "  ", payment_method_id, 2, 10)

    with pytest.raises(ValueError):
        insert_purchase(connection, "Ração", "31/05/2024", 125, 1, payment_method_id, "2", 10)

    with pytest.raises(ValueError):
        insert_purchase(connection, "Ração", "31/05/2024", 125, 1, payment_method_id, 2, -10)


def test_insert_purchase_with_nonexistent_payment_method_id(connection):
    with pytest.raises(sqlite3.IntegrityError):
        insert_purchase(connection, "Ração", "31/05/2024", 100, 1, 999, 2, 10)


def test_select_purchase_by_id(connection):
    payment_method_id = insert_payment_method(connection, "Nubank", 2, 25, 5)
    purchase_id = insert_purchase(connection, "Ração", "31/05/2024", 123, 1, payment_method_id, 2, 10)

    selected_purchase = select_purchase_by_id(connection, purchase_id)
    assert selected_purchase[0] ==  purchase_id # id
    assert selected_purchase[1] == "Ração" # description
    assert selected_purchase[2] == "2024-05-31" # purchase_date
    assert selected_purchase[3] == 123 # value
    assert selected_purchase[4] == 1 # installment_count
    assert selected_purchase[5] == payment_method_id # payment_method_id
    assert selected_purchase[6] == 2 # category_id
    assert selected_purchase[7] == 10 # subcategory_id
    assert selected_purchase[8] is not None # created_at
    assert selected_purchase[9] is None # updated_at
    assert selected_purchase[10] == 0 # removed


def test_select_purchase_by_id_with_invalid_id(connection):
    with pytest.raises(ValueError):
        select_purchase_by_id(connection, None)

    with pytest.raises(ValueError):
        select_purchase_by_id(connection, True)

    with pytest.raises(ValueError):
        select_purchase_by_id(connection, "1")

    with pytest.raises(ValueError):
        select_purchase_by_id(connection, 0)

    with pytest.raises(ValueError):
        select_purchase_by_id(connection, -1)


def test_select_purchase_by_id_with_nonexistent_id(connection):
    assert select_purchase_by_id(connection, 9872) is None



