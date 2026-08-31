import sqlite3

from app.services.validation import validate_and_convert_date, validate_positive_integer, validate_transaction_status

def insert_transaction(connection, purchase_id, person_id, installment, value, due_date, status):
    validate_positive_integer(purchase_id, "purchase_id")
    validate_positive_integer(person_id, "person_id")
    validate_positive_integer(installment, "installment")
    validate_positive_integer(value, "value")

    due_date = validate_and_convert_date(due_date)
    validate_transaction_status(status)

    try:
        query = (
            "INSERT INTO transactions "
            "(purchase_id, person_id, installment, value, due_date, status) "
            "VALUES (?, ?, ?, ?, ?, ?)"
        )
        values = (purchase_id, person_id, installment, value, due_date, status)

        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()

        return cursor.lastrowid
    except sqlite3.Error:
        connection.rollback()
        raise



