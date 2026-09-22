from datetime import datetime

from app.services.validation import validate_and_convert_date, validate_positive_integer, validate_transaction_status, get_month_date_range


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


def select_transactions_details(connection, payment_method_id=None, due_month=None, order="DESC"):
    query = """
        SELECT t.id AS transaction_id,
        t.purchase_id,
        p.description AS purchase_description,
        p.purchase_date,
        p.installment_count,
        pm.id AS payment_method_id,
        pm.description AS payment_method_description,
        t.person_id,
        pp.name AS person_name,
        t.installment,
        t.value,
        t.due_date,
        t.payment_date,
        t.status
        FROM transactions AS t 
        JOIN purchases AS p ON t.purchase_id = p.id
        JOIN people AS pp ON pp.id = t.person_id 
        JOIN payment_methods AS pm ON p.payment_method_id = pm.id
        WHERE t.removed = ? AND p.removed = ?
    """

    values: list[int | str] = [0, 0]

    if payment_method_id is not None:
        validate_positive_integer(payment_method_id, "payment_method_id")

        query += " AND p.payment_method_id = ?"
        values.append(payment_method_id)

    if due_month is not None:
        start_date, end_date = get_month_date_range(due_month)

        query += " AND t.due_date >= ? AND t.due_date < ?"
        values.append(start_date)
        values.append(end_date)

    order = order.upper()
    if order not in ("ASC", "DESC"):
        raise ValueError("order must be ASC or DESC")

    query += f" ORDER BY t.id {order}"

    cursor = connection.cursor()
    cursor.execute(query, tuple(values))
    return cursor.fetchall()


def update_transaction_status(connection, transaction_id, status):
    validate_positive_integer(transaction_id, "transaction_id")
    validate_transaction_status(status)

    payment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status == 1 else None
    query = "UPDATE transactions SET status=?, payment_date=? WHERE id=? AND removed=0"
    values = (status, payment_date, transaction_id)

    cursor = connection.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise ValueError("transaction not found")


def select_oldest_pending_due_date(connection, payment_method_id):
    validate_positive_integer(payment_method_id, "payment_method_id")

    query = """SELECT t.due_date FROM transactions AS t JOIN purchases AS p ON t.purchase_id = p.id
    WHERE p.payment_method_id = ? AND t.removed = ? AND p.removed = ? AND t.status != ? ORDER BY t.due_date ASC LIMIT 1"""

    cursor = connection.cursor()
    cursor.execute(query, (payment_method_id, 0, 0, 1))

    return cursor.fetchone()

