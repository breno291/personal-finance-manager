import pytest

from app.database.transactions import *
from app.database.people import insert_person
from app.database.payment_methods import insert_payment_method
from app.database.purchases import insert_purchase

def test_insert_transaction(connection):
    person_id = insert_person(connection, "luciana")
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
    person_id = insert_person(connection, "Luciana")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(
        connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4
    )

    with pytest.raises(ValueError):
        insert_transaction(
            connection, "1", person_id, 1, 3221, "01/09/2026", 1
        )

    with pytest.raises(ValueError):
        insert_transaction(
            connection, purchase_id, "  ", 1, 3221, "01/09/2026", 1
        )

    with pytest.raises(ValueError):
        insert_transaction(
            connection, purchase_id, person_id, "1", 3221, "01/09/2026", 1
        )

    with pytest.raises(ValueError):
        insert_transaction(
            connection, purchase_id, person_id, 1, None, "01/09/2026", 1
        )


def test_insert_transaction_with_invalid_status(connection):
    person_id = insert_person(connection, "Luciana")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(
        connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4
    )

    with pytest.raises(ValueError):
        insert_transaction(
            connection, purchase_id, person_id, 1, 3221, "01/09/2026", -1
        )

    with pytest.raises(ValueError):
        insert_transaction(
            connection, purchase_id, person_id, 1, 3221, "01/09/2026", 4
        )

    with pytest.raises(ValueError):
        insert_transaction(
            connection, purchase_id, person_id, 1, 3221, "01/09/2026", "1"
        )

    with pytest.raises(ValueError):
        insert_transaction(
            connection, purchase_id, person_id, 1, 3221, "01/09/2026", True
        )

    with pytest.raises(ValueError):
        insert_transaction(
            connection, purchase_id, person_id, 1, 3221, "01/09/2026", None
        )


def test_insert_transaction_with_nonexistent_purchase_id(connection):
    person_id = insert_person(connection, "Luciana")

    with pytest.raises(sqlite3.IntegrityError):
        insert_transaction(
            connection, 999, person_id, 1, 3221, "01/09/2026", 1
        )


def test_insert_transaction_with_nonexistent_person_id(connection):
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(
        connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4
    )

    with pytest.raises(sqlite3.IntegrityError):
        insert_transaction(
            connection, purchase_id, 999, 1, 3221, "01/09/2026", 1
        )


def test_insert_transaction_with_invalid_due_date(connection):
    person_id = insert_person(connection, "Luciana")
    payment_method_id = insert_payment_method(connection, "PicPay", 2, 23, 6)
    purchase_id = insert_purchase(
        connection, "Ração", "05/12/2026", 3221, 1, payment_method_id, 2, 4
    )

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, person_id, 1, 3221, "31/02/2026", 1)

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, person_id, 1, 3221, None, 1)

    with pytest.raises(ValueError):
        insert_transaction(connection, purchase_id, person_id, 1, 3221, "31-05-2026", 1)




