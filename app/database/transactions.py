from app.services.validation import validate_and_convert_date, validate_positive_integer, validate_transaction_status


def insert_transaction(connection, purchase_id, person_id, installment, value, due_date, status):
    validate_positive_integer(purchase_id, "purchase_id")
    validate_positive_integer(person_id, "person_id")
    validate_positive_integer(installment, "installment")
    validate_positive_integer(value, "value")

    due_date = validate_and_convert_date(due_date)
    validate_transaction_status(status)

    query = ("INSERT INTO transactions (purchase_id, person_id, installment, value, due_date, status) VALUES (?, ?, ?, ?, ?, ?)")
    values = (purchase_id, person_id, installment, value, due_date, status)

    cursor = connection.cursor()
    cursor.execute(query, values)

    return cursor.lastrowid


def select_transaction_by_id(connection, transaction_id):
    validate_positive_integer(transaction_id, "transaction_id")

    query = ("SELECT id, purchase_id, person_id, installment, value, due_date, payment_date, status FROM transactions WHERE id = ? AND removed = ?")

    cursor = connection.cursor()
    cursor.execute(query, (transaction_id, 0))

    return cursor.fetchone()


def select_transactions(connection):
    query = ("SELECT id, purchase_id, person_id, installment, value, due_date, payment_date, status FROM transactions WHERE removed = ? ORDER BY id DESC")

    cursor = connection.cursor()
    cursor.execute(query, (0,))

    return cursor.fetchall()


def update_transaction(connection, transaction_id, purchase_id, person_id, installment, value, due_date):
    validate_positive_integer(transaction_id, "transaction_id")
    validate_positive_integer(purchase_id, "purchase_id")
    validate_positive_integer(person_id, "person_id")
    validate_positive_integer(installment, "installment")
    validate_positive_integer(value, "value")

    due_date = validate_and_convert_date(due_date)

    query = ("UPDATE transactions SET purchase_id=?, person_id=?, installment=?, value=?, due_date=? WHERE id=?")
    values = (purchase_id, person_id, installment, value, due_date, transaction_id)

    cursor = connection.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise ValueError("transaction not found")


def remove_transaction(connection, transaction_id):
    validate_positive_integer(transaction_id, "transaction_id")

    query = "UPDATE transactions SET removed=? WHERE id=?"
    values = (1, transaction_id)

    cursor = connection.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise ValueError("transaction not found")


def select_transactions_by_purchase_id(connection, purchase_id):
    validate_positive_integer(purchase_id, "purchase_id")

    query = ("SELECT id, purchase_id, person_id, installment, value, due_date, payment_date, status FROM transactions WHERE purchase_id = ? AND removed = ?")

    cursor = connection.cursor()
    cursor.execute(query, (purchase_id, 0))

    return cursor.fetchall()



