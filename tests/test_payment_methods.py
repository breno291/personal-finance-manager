import pytest
from app.database.payment_methods import *
from app.config import CASH, CREDIT


# ==================================================
# INSERT PAYMENT METHOD
# ==================================================

def test_insert_payment_method(connection):
    payment_method_id = insert_payment_method(connection, "Nubank", CREDIT, 25, 5)
    assert payment_method_id is not None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM payment_methods WHERE id = ?", (payment_method_id,))
    payment = cursor.fetchone()

    assert payment[0] == payment_method_id # "id
    assert payment[1] == "Nubank" # description
    assert payment[2] == CREDIT # payment_type
    assert payment[3] == 25 # closing_day
    assert payment[4] == 5 # due_day
    assert payment[5] == 0 # removed


def test_insert_payment_method_without_description(connection):
    with pytest.raises(ValueError):
        insert_payment_method(connection, "  ", CREDIT, 25, 5)
    with pytest.raises(ValueError):
        insert_payment_method(connection, None, CREDIT, 25, 5)
    with pytest.raises(ValueError):
        insert_payment_method(connection, 123, CREDIT, 25, 5)


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
        insert_payment_method(connection, "Caixa", CREDIT, "25", 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", CREDIT, 25, "5")

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", CREDIT, 0, 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", CREDIT, 25, 0)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", CREDIT, -1, 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", CREDIT, 25, -1)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", CREDIT, 32, 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", CREDIT, 25, 32)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", CREDIT, None, 5)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", CREDIT, 25, None)

    with pytest.raises(ValueError):
        insert_payment_method(connection, "Caixa", CREDIT, 17, 17)


def test_insert_payment_method_with_null_days(connection):
    payment_method_id = insert_payment_method(connection, "Nubank", CASH, None, None)
    assert payment_method_id is not None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM payment_methods WHERE id = ?", (payment_method_id,))
    payment = cursor.fetchone()

    assert payment[0] == payment_method_id # "id
    assert payment[1] == "Nubank" # description
    assert payment[2] == CASH # payment_type
    assert payment[3] is None # closing_day
    assert payment[4] is None # due_day
    assert payment[5] == 0 # removed


# ==================================================
# SELECT PAYMENT METHOD BY ID
# ==================================================

def test_select_payment_method_by_id(connection):
    payment_method_id = insert_payment_method(connection, "Santander", CREDIT, 26, 4)

    payment_method = select_payment_method_by_id(connection, payment_method_id)

    assert payment_method[0] == payment_method_id # "id
    assert payment_method[1] == "Santander" # description
    assert payment_method[2] == CREDIT # payment_type
    assert payment_method[3] == 26 # closing_day
    assert payment_method[4] == 4 # due_day


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


def test_select_payment_method_by_id_with_removed_payment_method(connection):
    payment_method_id = insert_payment_method(connection, "Santander", CREDIT, 26, 4)

    cursor = connection.cursor()
    cursor.execute("UPDATE payment_methods SET removed = 1 WHERE id = ?", (payment_method_id,))
    connection.commit()

    payment_method = select_payment_method_by_id(connection, payment_method_id)

    assert payment_method is None


# ==================================================
# SELECT PAYMENT METHODS
# ==================================================

def test_select_payment_methods(connection):
    insert_payment_method(connection, "PicPay", CASH, 5, 25)
    insert_payment_method(connection, "Caixa", CREDIT, 5, 25)
    insert_payment_method(connection, "Nubank", CASH, 15, 25)

    payment_methods = select_payment_methods(connection)

    assert len(payment_methods) == 3
    assert payment_methods[0][2] == CASH
    assert payment_methods[1][3] == 5
    assert payment_methods[2][1] == "Nubank"


def test_select_payment_methods_excludes_removed(connection):
    insert_payment_method(connection, "PicPay", CASH, 15, 25)
    payment_method_id = insert_payment_method(connection, "Santander", CASH, 26, 4)
    insert_payment_method(connection, "Nubank", CREDIT, 15, 25)


    cursor = connection.cursor()
    cursor.execute("UPDATE payment_methods SET removed = 1 WHERE id = ?", (payment_method_id,))
    connection.commit()

    payment_methods = select_payment_methods(connection)

    assert len(payment_methods) == 2
    assert payment_methods[0][1] == "PicPay"
    assert payment_methods[1][2] == CREDIT
    assert payment_methods[1][0] == 3


def test_select_payment_methods_empty(connection):
    payment_methods = select_payment_methods(connection)

    assert len(payment_methods) == 0


def test_select_payment_methods_with_pagination(connection):
    page = 1
    total_number_of_items = 6

    for i in range(10):
        insert_payment_method(connection, f"test_{i}", CASH, 26, 4)

    payment_methods = select_payment_methods(connection, page, total_number_of_items)

    assert len(payment_methods) == total_number_of_items
    assert payment_methods[0][1] == "test_9"
    assert payment_methods[1][1] == "test_8"
    assert payment_methods[2][1] == "test_7"
    assert payment_methods[3][1] == "test_6"
    assert payment_methods[4][1] == "test_5"
    assert payment_methods[5][1] == "test_4"

    page = 2
    payment_methods = select_payment_methods(connection, page, total_number_of_items)

    assert len(payment_methods) == 4
    assert payment_methods[0][1] == "test_3"
    assert payment_methods[1][1] == "test_2"
    assert payment_methods[2][1] == "test_1"
    assert payment_methods[3][1] == "test_0"


def test_select_payment_methods_with_invalid_page(connection):
    with pytest.raises(ValueError):
        select_payment_methods(connection, 0, 6)

    with pytest.raises(ValueError):
        select_payment_methods(connection, -1, 6)

    with pytest.raises(ValueError):
        select_payment_methods(connection, "1", 6)

    with pytest.raises(ValueError):
        select_payment_methods(connection, True, 6)


def test_select_payment_methods_with_invalid_total_number_of_items(connection):
    with pytest.raises(ValueError):
        select_payment_methods(connection, 1, 0)

    with pytest.raises(ValueError):
        select_payment_methods(connection, 1, -1)

    with pytest.raises(ValueError):
        select_payment_methods(connection, 1, "6")

    with pytest.raises(ValueError):
        select_payment_methods(connection, 1, True)


def test_select_payment_methods_with_search(connection):
    insert_payment_method(connection, "PicPay", CASH, 5, 25)
    insert_payment_method(connection, "Caixa", CREDIT, 25, 28)
    payment_method_id = insert_payment_method(connection, "Brasil", CREDIT, 26, 4)
    insert_payment_method(connection, "Bradesco", CASH, 15, 25)

    payment_methods = select_payment_methods(connection, search="PicPay")

    assert payment_methods[0][1] == "PicPay"
    assert payment_methods[0][2] == CASH
    assert payment_methods[0][3] == 5
    assert payment_methods[0][4] == 25

    payment_methods = select_payment_methods(connection, search="Bra")

    assert payment_methods[0][1] == "Brasil"
    assert payment_methods[0][2] == CREDIT
    assert payment_methods[0][3] == 26
    assert payment_methods[0][4] == 4

    assert payment_methods[1][1] == "Bradesco"
    assert payment_methods[1][2] == CASH
    assert payment_methods[1][3] == 15
    assert payment_methods[1][4] == 25

    cursor = connection.cursor()
    cursor.execute("UPDATE payment_methods SET removed = 1 WHERE id = ?", (payment_method_id,))
    connection.commit()

    payment_methods = select_payment_methods(connection, search="Bra")

    assert payment_methods[0][1] == "Bradesco"
    assert payment_methods[0][2] == CASH
    assert payment_methods[0][3] == 15
    assert payment_methods[0][4] == 25


def test_select_payment_methods_with_search_and_pagination(connection):
    for i in range(10):
        insert_payment_method(connection, f"Teste {i}", CASH, 26, 4)

    insert_payment_method(connection, "Nubank", CASH, 13, 31)

    payment_methods = select_payment_methods(connection, page=1, total_number_of_items=6, search="teste")

    assert len(payment_methods) == 6
    assert payment_methods[0][1] == "Teste 9"
    assert payment_methods[5][1] == "Teste 4"

    payment_methods = select_payment_methods(connection, page=2, total_number_of_items=6, search="Teste")

    assert len(payment_methods) == 4
    assert payment_methods[0][1] == "Teste 3"
    assert payment_methods[3][1] == "Teste 0"


# ==================================================
# COUNT PAYMENT METHODS
# ==================================================

def test_count_payment_methods(connection):
    assert count_payment_methods(connection) == 0

    for i in range(3):
        insert_payment_method(connection, f"test_{i}", CASH, 26, 4)

    assert count_payment_methods(connection) == 3

    payment_method_id = insert_payment_method(connection, "Brasil", CREDIT, 26, 4)

    assert count_payment_methods(connection) == 4

    cursor = connection.cursor()
    cursor.execute("UPDATE payment_methods SET removed = 1 WHERE id = ?", (payment_method_id,))
    connection.commit()

    assert count_payment_methods(connection) == 3


def test_count_payment_methods_with_search(connection):
    insert_payment_method(connection, "Brasil", CASH, 5, 25)
    insert_payment_method(connection, "Caixa", CREDIT, 25, 28)
    insert_payment_method(connection, "Bradesco", CASH, 15, 25)

    assert count_payment_methods(connection, search="Bra") == 2
    assert count_payment_methods(connection, search="Caixa") == 1
    assert count_payment_methods(connection, search="PicPay") == 0


# ==================================================
# UPDATE PAYMENT METHODS
# ==================================================

def test_update_payment_methods(connection):
    payment_method_id = insert_payment_method(connection, "Brasil", CREDIT, 26, 4)

    update_payment_method(connection, payment_method_id, "PicPay", CASH, 5, 30)

    payment_methods = select_payment_method_by_id(connection, payment_method_id)

    assert payment_methods[1] == "PicPay"
    assert payment_methods[2] == CASH
    assert payment_methods[3] == 5
    assert payment_methods[4] == 30


def test_update_payment_methods_with_nonexistent_id(connection):
    with pytest.raises(ValueError):
        update_payment_method(connection, 9999, "PicPay", CASH, 5, 30)


def test_update_payment_methods_with_invalid_id(connection):
    with pytest.raises(ValueError):
        update_payment_method(connection, 0, "PicPay", CASH, 5, 30)


def test_update_payment_methods_with_invalid_payment_type(connection):
    payment_method_id = insert_payment_method(connection, "Brasil", CREDIT, 26, 4)

    with pytest.raises(ValueError):
        update_payment_method(connection, payment_method_id, "PicPay", -1, 5, 30)


# ==================================================
# REMOVE PAYMENT METHOD
# ==================================================

def test_remove_payment_method(connection):
    payment_method_id = insert_payment_method(connection, "Brasil", CREDIT, 26, 4)

    remove_payment_method(connection, payment_method_id)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM payment_methods WHERE id = ?", (payment_method_id,))
    payment_method = cursor.fetchone()

    assert payment_method[5] == 1


def test_remove_payment_method_with_nonexistent_id(connection):
    with pytest.raises(ValueError):
        remove_payment_method(connection, 9999)


def test_remove_payment_method_with_invalid_id(connection):
    with pytest.raises(ValueError):
        remove_payment_method(connection, -1)


