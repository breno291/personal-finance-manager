import sqlite3

import pytest

from app.database.transactions import *
from app.database.people import insert_person
from app.database.payment_methods import insert_payment_method
from app.database.purchases import insert_purchase


# ==================================================
# INSERT TRANSACTION
# ==================================================

def test_insert_transaction(connection):
    person_id = insert_person(connection, "luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)
    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", 1)

    assert transaction_id is not None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))

    transaction = cursor.fetchone()
    assert transaction[0] == transaction_id  # id
    assert transaction[1] == purchase_id # purchase_id
    assert transaction[2] == person_id # person_id
    assert transaction[3] == 1 # installment
    assert transaction[4] == 3221 # value
    assert transaction[5] == "2026-09-01" # due_date
    assert transaction[6] is None  # payment_date
    assert transaction[7] == 1 # status
    assert transaction[8] == 0 # removed


def test_insert_transaction_with_invalid_positive_integer(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)

    with pytest.raises(ValueError):
        insert_transaction(connection, "1", person_id, 1, 3221, "01/09/2026", 1)

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, "  ", 1, 3221, "01/09/2026", 1)

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, person_id, "1", 3221, "01/09/2026", 1)

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, person_id, 1, None, "01/09/2026", 1)


def test_insert_transaction_with_invalid_status(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", -1)

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", 4)

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", "1")

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", True)

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", None)


def test_insert_transaction_with_nonexistent_purchase_id(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")

    with pytest.raises(sqlite3.IntegrityError):
        insert_transaction(connection, 999, person_id, 1, 3221, "01/09/2026", 1)


def test_insert_transaction_with_nonexistent_person_id(connection):
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)

    with pytest.raises(sqlite3.IntegrityError):
        insert_transaction(connection, purchase_id, 999, 1, 3221, "01/09/2026", 1)


def test_insert_transaction_with_invalid_due_date(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, person_id, 1, 3221, "31/02/2026", 1)

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, person_id, 1, 3221, None, 1)

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, person_id, 1, 3221, "31-05-2026", 1)


# ==================================================
# SELECT TRANSACTION BY ID
# ==================================================

def test_select_transaction_by_id(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)
    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", 0)

    transaction = select_transaction_by_id(connection, transaction_id)

    assert transaction[0] == transaction_id
    assert transaction[1] == purchase_id
    assert transaction[2] == person_id
    assert transaction[3] == 1
    assert transaction[4] == 3221
    assert transaction[5] == "2026-09-01"
    assert transaction[6] is None
    assert transaction[7] == 0


def test_select_transaction_by_id_with_invalid_id(connection):
    with pytest.raises(ValueError):
        select_transaction_by_id(connection, -1)

    with pytest.raises(ValueError):
        select_transaction_by_id(connection, 0)


def test_select_transaction_by_id_with_nonexistent_id(connection):
    assert select_transaction_by_id(connection, 9999) is None


def test_select_transaction_by_id_with_removed_transaction(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)
    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", 0)

    remove_transaction(connection, transaction_id)

    transaction = select_transaction_by_id(connection, transaction_id)

    assert transaction is None


# ==================================================
# SELECT TRANSACTIONS
# ==================================================

def test_select_transactions(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 2, payment_method_id, 2, 4)

    insert_transaction(connection, purchase_id, person_id, 1, 1611, "01/09/2026", 0)
    insert_transaction(connection, purchase_id, person_id, 2, 1610, "01/10/2026", 0)

    transactions = select_transactions(connection)

    assert len(transactions) == 2
    assert transactions[0][3] == 2
    assert transactions[1][3] == 1


def test_select_transactions_returns_empty_list(connection):
    transactions = select_transactions(connection)

    assert transactions == []


def test_select_transactions_does_not_return_removed_transaction(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)
    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", 0)

    remove_transaction(connection, transaction_id)

    transactions = select_transactions(connection)

    assert transactions == []


# ==================================================
# UPDATE TRANSACTION
# ==================================================

def test_update_transaction(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    person_id_2 = insert_person(connection, "Breno", "breno@email.com", "81999999999")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 2, payment_method_id, 2, 4)
    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 1611, "01/09/2026", 0)

    update_transaction(connection, transaction_id, purchase_id, person_id_2, 2, 2000, "01/10/2026")

    transaction = select_transaction_by_id(connection, transaction_id)

    assert transaction[0] == transaction_id
    assert transaction[1] == purchase_id
    assert transaction[2] == person_id_2
    assert transaction[3] == 2
    assert transaction[4] == 2000
    assert transaction[5] == "2026-10-01"


def test_update_transaction_with_invalid_id(connection):
    with pytest.raises(ValueError):
        update_transaction(connection, -1, 1, 1, 1, 1000, "01/09/2026")


def test_update_transaction_with_nonexistent_id(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)

    with pytest.raises(ValueError):
        update_transaction(connection, 9999, purchase_id, person_id, 1, 3221, "01/09/2026")


# ==================================================
# REMOVE TRANSACTION
# ==================================================

def test_remove_transaction(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)
    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", 0)

    remove_transaction(connection, transaction_id)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
    transaction = cursor.fetchone()

    assert transaction[8] == 1


def test_remove_transaction_with_invalid_id(connection):
    with pytest.raises(ValueError):
        remove_transaction(connection, -1)


def test_remove_transaction_with_nonexistent_id(connection):
    with pytest.raises(ValueError):
        remove_transaction(connection, 9999)


# ==================================================
# SELECT TRANSACTIONS BY PURCHASE ID
# ==================================================

def test_select_transactions_by_purchase_id(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 2, payment_method_id, 2, 4)

    transaction_id_1 = insert_transaction(connection, purchase_id, person_id, 1, 1611, "01/09/2026", 0)
    transaction_id_2 = insert_transaction(connection, purchase_id, person_id, 2, 1610, "01/10/2026", 0)

    transactions = select_transactions_by_purchase_id(connection, purchase_id)

    assert len(transactions) == 2
    assert transactions[0][0] == transaction_id_1
    assert transactions[0][1] == purchase_id
    assert transactions[1][0] == transaction_id_2
    assert transactions[1][1] == purchase_id


def test_select_transactions_by_purchase_id_does_not_return_another_purchase(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)

    purchase_id_1 = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)
    purchase_id_2 = insert_purchase(connection, "Gasolina", "05/12/2026", 5000, 1, payment_method_id, 6, 16)

    insert_transaction(connection, purchase_id_1, person_id, 1, 3221, "01/09/2026", 0)
    insert_transaction(connection, purchase_id_2, person_id, 1, 5000, "01/09/2026", 0)

    transactions = select_transactions_by_purchase_id(connection, purchase_id_1)

    assert len(transactions) == 1
    assert transactions[0][1] == purchase_id_1


def test_select_transactions_by_purchase_id_does_not_return_removed_transaction(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)

    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", 0)

    remove_transaction(connection, transaction_id)

    transactions = select_transactions_by_purchase_id(connection, purchase_id)

    assert transactions == []


def test_select_transactions_by_purchase_id_with_invalid_id(connection):
    with pytest.raises(ValueError):
        select_transactions_by_purchase_id(connection, -1)

    with pytest.raises(ValueError):
        select_transactions_by_purchase_id(connection, 0)


def test_select_transactions_by_purchase_id_with_nonexistent_id(connection):
    transactions = select_transactions_by_purchase_id(connection, 9999)

    assert transactions == []



