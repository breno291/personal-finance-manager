import sqlite3

from app.services.validation import validate_required_string, validate_and_convert_date, validate_positive_integer

def insert_purchase(connection, description, purchase_date, value, installment_count, payment_method_id, category_id, subcategory_id):
    validate_required_string(description, "description")
    purchase_date = validate_and_convert_date(purchase_date)

    validate_positive_integer(value, "value")
    validate_positive_integer(installment_count, "installment_count")
    validate_positive_integer(payment_method_id, "payment_method_id")
    validate_positive_integer(category_id, "category_id")
    validate_positive_integer(subcategory_id, "subcategory_id")

    try:
        description = description.strip()
        query = (
            "INSERT INTO purchases "
            "(description, purchase_date, value, installment_count, "
            "payment_method_id, category_id, subcategory_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)"
        )
        values = (description, purchase_date, value, installment_count, payment_method_id, category_id, subcategory_id)

        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()

        return cursor.lastrowid

    except sqlite3.Error:
        connection.rollback()
        raise

def select_purchase_by_id(connection, purchase_id):
    validate_positive_integer(purchase_id, "purchase_id")

    query = "SELECT * FROM purchases WHERE id = ?"
    cursor = connection.cursor()
    cursor.execute(query, (purchase_id,))

    return cursor.fetchone()



