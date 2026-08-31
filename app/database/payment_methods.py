import sqlite3
from app.services.validation import validate_required_string, validate_positive_integer, validate_payment_days

def insert_payment_method(connection, description, payment_type, closing_day, due_day):
    validate_required_string(description, "description")
    validate_positive_integer(payment_type, "payment_type")
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

    query = "SELECT * FROM payment_methods WHERE id = ?"
    cursor = connection.cursor()
    cursor.execute(query, (payment_method_id,))

    return cursor.fetchone()



