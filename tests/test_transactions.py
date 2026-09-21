import sqlite3

import pytest

from datetime import date

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


# ==================================================
# SELECT TRANSACTIONS DETAILS
# ==================================================

def test_select_transactions_details(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 2, payment_method_id, 2, 4)

    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 1611, "01/09/2026", 0)

    transactions = select_transactions_details(connection)

    assert len(transactions) == 1

    transaction = transactions[0]

    assert transaction[0] == transaction_id
    assert transaction[1] == purchase_id
    assert transaction[2] == "Ração"
    assert transaction[3] == "2026-12-05"
    assert transaction[4] == 2
    assert transaction[5] == payment_method_id
    assert transaction[6] == "PicPay"
    assert transaction[7] == person_id
    assert transaction[8] == "Luciana"
    assert transaction[9] == 1
    assert transaction[10] == 1611
    assert transaction[11] == "2026-09-01"
    assert transaction[12] is None
    assert transaction[13] == 0


def test_select_transactions_details_returns_empty_list(connection):
    transactions = select_transactions_details(connection)

    assert transactions == []


def test_select_transactions_details_does_not_return_removed_transaction(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)
    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", 0)

    remove_transaction(connection, transaction_id)

    transactions = select_transactions_details(connection)

    assert transactions == []


def test_select_transactions_details_order(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 2, payment_method_id, 2, 4)

    transaction_id_1 = insert_transaction(connection, purchase_id, person_id, 1, 1611, "01/09/2026", 0)
    transaction_id_2 = insert_transaction(connection, purchase_id, person_id, 2, 1610, "01/10/2026", 0)

    transactions_asc = select_transactions_details(connection, "ASC")
    transactions_desc = select_transactions_details(connection, "DESC")

    assert transactions_asc[0][0] == transaction_id_1
    assert transactions_asc[1][0] == transaction_id_2

    assert transactions_desc[0][0] == transaction_id_2
    assert transactions_desc[1][0] == transaction_id_1


# ==================================================
# UPDATE TRANSACTIONS STATUS
# ==================================================

def test_update_transaction_status_to_paid(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)
    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", 0)

    update_transaction_status(connection, transaction_id, 1)

    transaction = select_transaction_by_id(connection, transaction_id)

    assert transaction["status"] == 1
    assert transaction["payment_date"][:10] == date.today().isoformat()


def test_update_transaction_status_to_separated(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)
    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", 0)

    update_transaction_status(connection, transaction_id, 2)

    transaction = select_transaction_by_id(connection, transaction_id)

    assert transaction["status"] == 2
    assert transaction["payment_date"] is None


def test_update_transaction_status_to_not_paid(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)
    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", 0)

    update_transaction_status(connection, transaction_id, 1)
    update_transaction_status(connection, transaction_id, 0)

    transaction = select_transaction_by_id(connection, transaction_id)

    assert transaction["status"] == 0
    assert transaction["payment_date"] is None


def test_update_transaction_status_removes_payment_date_when_changed_to_separated(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)
    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", 0)

    update_transaction_status(connection, transaction_id, 1)
    update_transaction_status(connection, transaction_id, 2)

    transaction = select_transaction_by_id(connection, transaction_id)

    assert transaction["status"] == 2
    assert transaction["payment_date"] is None


def test_update_transaction_status_with_invalid_status(connection):
    with pytest.raises(ValueError):
        update_transaction_status(connection, 1, -1)

    with pytest.raises(ValueError):
        update_transaction_status(connection, 1, 3)

    with pytest.raises(ValueError):
        update_transaction_status(connection, 1, "1")

    with pytest.raises(ValueError):
        update_transaction_status(connection, 1, True)


def test_update_transaction_status_with_invalid_transaction_id(connection):
    with pytest.raises(ValueError):
        update_transaction_status(connection, 0, 1)

    with pytest.raises(ValueError):
        update_transaction_status(connection, -1, 1)

    with pytest.raises(ValueError):
        update_transaction_status(connection, "1", 1)

    with pytest.raises(ValueError):
        update_transaction_status(connection, True, 1)


def test_update_transaction_status_when_transaction_not_found(connection):
    with pytest.raises(ValueError):
        update_transaction_status(connection, 999, 1)


def test_update_transaction_status_when_transaction_is_removed(connection):
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81988888888")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4)
    transaction_id = insert_transaction(connection, purchase_id, person_id, 1, 3221, "01/09/2026", 0)

    remove_transaction(connection, transaction_id)

    with pytest.raises(ValueError):
        update_transaction_status(connection, transaction_id, 1)

