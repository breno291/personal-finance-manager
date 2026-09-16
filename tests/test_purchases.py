import pytest
import sqlite3

from app.database.purchases import *
from app.database.payment_methods import insert_payment_method
from app.database.transactions import insert_transaction
from app.database.people import insert_person

# ==================================================
# INSERT PURCHASE
# ==================================================

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


# ==================================================
# SELECT PURCHASE BY ID
# ==================================================

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


def test_select_purchase_by_id_with_removed_purchase(connection):
    payment_method_id = insert_payment_method(connection, "Nubank", 2, 25, 5)
    purchase_id = insert_purchase(connection, "Ração", "31/05/2024", 123, 1, payment_method_id, 2, 10)

    cursor = connection.cursor()
    cursor.execute("UPDATE purchases SET removed = 1 WHERE id = ?", (purchase_id,))
    connection.commit()

    purchase = select_purchase_by_id(connection, purchase_id)

    assert purchase is None


# ==================================================
# SELECT PURCHASES
# ==================================================

def test_select_purchases_for_management(connection):
    payment_method_id = insert_payment_method(connection, "Nubank", 2, 25, 5)
    insert_purchase(connection, "   Ração   ", "30/08/2026", 1550, 1, payment_method_id, 2, 10)

    purchases = select_purchases_for_management(connection)

    assert purchases[0][1] == "Ração" # description
    assert purchases[0][2] == "2026-08-30" # purchase_date
    assert purchases[0][3] == 1550 # value
    assert purchases[0][4] == 1 # installment_count
    assert purchases[0][5] == payment_method_id # payment_method_id
    assert purchases[0][6] == "Nubank" # payment_method
    assert purchases[0][7] == 2 # category_id
    assert purchases[0][8] == 10 # subcategory_id
    assert purchases[0][9] is not None # created_at
    assert purchases[0][10] is None # updated_at


def test_select_purchases_for_management_returns_empty_list(connection):
    purchases = select_purchases_for_management(connection)
    assert purchases == []


def test_select_purchases_for_management_returns_multiple_purchases(connection):
    payment_method_id = insert_payment_method(connection, "Nubank", 2, 25, 5)

    insert_purchase(connection, "Ração", "30/08/2026", 1550, 1, payment_method_id, 2, 10)
    insert_purchase(connection, "Gasolina", "31/08/2026", 5000, 1, payment_method_id, 6, 16)

    purchases = select_purchases_for_management(connection)

    assert len(purchases) == 2


def test_select_purchases_for_management_does_not_return_removed_purchase(connection):
    payment_method_id = insert_payment_method(connection, "Nubank", 2, 25, 5)
    purchase_id = insert_purchase(connection, "Ração", "30/08/2026", 1550, 1, payment_method_id, 2, 10)

    connection.execute("UPDATE purchases SET removed = ? WHERE id = ?", (1, purchase_id))
    connection.commit()

    purchases = select_purchases_for_management(connection)
    assert purchases == []


# ==================================================
# UPDATE PURCHASE
# ==================================================

def test_update_purchase(connection):
    payment_method_id = insert_payment_method(connection, "Brasil", 2, 26, 4)
    purchase_id = insert_purchase(connection, "Ração", "30/08/2026", 1550, 1, payment_method_id, 2, 10)

    update_purchase(connection, purchase_id, "Comida", "01/09/2026", 9000, 2, payment_method_id, 4, 11)

    purchase = select_purchase_by_id(connection, purchase_id)
    assert purchase[0] ==  purchase_id # id
    assert purchase[1] == "Comida" # description
    assert purchase[2] == "2026-09-01" # purchase_date
    assert purchase[3] == 9000 # value
    assert purchase[4] == 2 # installment_count
    assert purchase[5] == payment_method_id # payment_method_id
    assert purchase[6] == 4 # category_id
    assert purchase[7] == 11 # subcategory_id
    assert purchase[8] is not None # created_at
    assert purchase[9] is not None # updated_at


def test_update_purchases_with_invalid_id(connection):
    payment_method_id = insert_payment_method(connection, "Brasil", 2, 26, 4)
    with pytest.raises(ValueError):
        update_purchase(connection, 0, "Comida", "01/09/2026", 9000, 2, payment_method_id, 4, 11)

    with pytest.raises(ValueError):
        update_purchase(connection, -1, "Comida", "01/09/2026", 9000, 2, payment_method_id, 4, 11)


def test_update_purchases_with_nonexistent_id(connection):
    payment_method_id = insert_payment_method(connection, "Brasil", 2, 26, 4)
    with pytest.raises(ValueError):
        update_purchase(connection, 9999, "Comida", "01/09/2026", 9000, 2, payment_method_id, 4, 11)


# ==================================================
# REMOVE PURCHASE
# ==================================================

def test_remove_purchase(connection):
    payment_method_id = insert_payment_method(connection, "Brasil", 2, 26, 4)
    purchase_id = insert_purchase(connection, "Ração", "30/08/2026", 1550, 1, payment_method_id, 2, 10)

    remove_purchase(connection, purchase_id)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM purchases WHERE id = ?", (purchase_id,))
    purchase = cursor.fetchone()

    assert purchase[9] is not None
    assert purchase[10] == 1


def test_remove_purchase_with_invalid_id(connection):
    with pytest.raises(ValueError):
        remove_purchase(connection, -1)


def test_remove_purchase_with_nonexistent_id(connection):
    with pytest.raises(ValueError):
        remove_purchase(connection, 9999)

