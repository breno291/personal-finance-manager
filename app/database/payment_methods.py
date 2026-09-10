import sqlite3
from app.services.validation import validate_required_string, validate_positive_integer, validate_payment_days, validate_integer_range, validate_credit_payment_days
from app.config import CREDIT, CASH

def insert_payment_method(connection, description, payment_type, closing_day, due_day):
    validate_required_string(description, "description")
    validate_integer_range(payment_type, "payment_type", CASH, CREDIT)
    validate_credit_payment_days(payment_type, closing_day, due_day)
    validate_payment_days(closing_day, due_day)

    try:
        description = description.strip()
        query = (
            "INSERT INTO payment_methods "
            "(description, payment_type, closing_day, due_day) "
            "VALUES (?, ?, ?, ?)"
        )
        values = (description, payment_type, closing_day, due_day)

        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()

        return cursor.lastrowid
    except sqlite3.Error:
        connection.rollback()
        raise


def select_payment_method_by_id(connection, payment_method_id):
    validate_positive_integer(payment_method_id, "payment_method_id")

    query = "SELECT id, description, payment_type, closing_day, due_day FROM payment_methods WHERE id = ? AND removed = ?"
    cursor = connection.cursor()
    cursor.execute(query, (payment_method_id, 0))

    return cursor.fetchone()


def select_payment_methods(connection, page=None, total_number_of_items=None, search=None):
    query = "SELECT id, description, payment_type, closing_day, due_day FROM payment_methods WHERE removed = ?"
    values = []
    values.append(0)

    if search is not None:
        query += " AND description LIKE ?"
        values.append(f"%{search}%")

    if page is not None and total_number_of_items is not None:
        validate_positive_integer(page, "page")
        validate_positive_integer(total_number_of_items, "total_number_of_items")

        offset = (page - 1) * total_number_of_items
        query += " ORDER BY id DESC LIMIT ? OFFSET ?"
        values.extend([total_number_of_items, offset])

    cursor = connection.cursor()
    cursor.execute(query, tuple(values))

    return cursor.fetchall()


def count_payment_methods(connection, search=None):
    query = "SELECT COUNT(id) FROM payment_methods WHERE removed = ?"
    values = []
    values.append(0)

    if search is not None:
        query += " AND description LIKE ?"
        values.append(f"%{search}%")

    cursor = connection.cursor()
    cursor.execute(query, values)

    return cursor.fetchone()[0]


def update_payment_method(connection, payment_method_id, description, payment_type, closing_day, due_day):
    validate_required_string(description, "description")
    validate_integer_range(payment_type, "payment_type", CASH, CREDIT)
    validate_credit_payment_days(payment_type, closing_day, due_day)
    validate_payment_days(closing_day, due_day)


    try:
        description = description.strip()
        query = "UPDATE payment_methods SET description=?, payment_type=?, closing_day=?, due_day=? WHERE id=?"
        values = (description, payment_type, closing_day, due_day, payment_method_id)

        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()

        if cursor.rowcount == 0:
            raise ValueError("payment_method not found")

    except sqlite3.Error:
        connection.rollback()
        raise


def remove_payment_method(connection, payment_method_id):
    validate_positive_integer(payment_method_id, "payment_method_id")

    try:
        query = "UPDATE payment_methods SET removed=? WHERE id=?"
        values = (1, payment_method_id)

        cursor = connection.cursor()
        cursor.execute(query, values)
        if cursor.rowcount == 0:
            raise ValueError("payment_methods not found")

        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        raise


