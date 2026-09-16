from app.services.validation import validate_required_string, validate_and_convert_date, validate_positive_integer


def insert_purchase(connection, description, purchase_date, value, installment_count, payment_method_id, category_id, subcategory_id):
    validate_required_string(description, "description")
    purchase_date = validate_and_convert_date(purchase_date)

    validate_positive_integer(value, "value")
    validate_positive_integer(installment_count, "installment_count")
    validate_positive_integer(payment_method_id, "payment_method_id")
    validate_positive_integer(category_id, "category_id")
    validate_positive_integer(subcategory_id, "subcategory_id")

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

    return cursor.lastrowid


def select_purchase_by_id(connection, purchase_id):
    validate_positive_integer(purchase_id, "purchase_id")

    query = "SELECT id, description, purchase_date, value, installment_count, payment_method_id, category_id, subcategory_id, created_at, updated_at"
    query += " FROM purchases WHERE id = ? AND removed = ?"
    cursor = connection.cursor()
    cursor.execute(query, (purchase_id, 0))

    return cursor.fetchone()


def select_purchases_for_management(connection):
    select = "SELECT p.id, p.description, p.purchase_date, p.value, p.installment_count, p.payment_method_id, pm.description AS payment_method, p.category_id, p.subcategory_id, p.created_at, p.updated_at"
    tables = " FROM purchases AS p JOIN payment_methods AS pm ON pm.id = p.payment_method_id"
    where = " WHERE p.removed = ? ORDER BY p.id DESC"
    query = select+tables+where

    cursor = connection.cursor()
    cursor.execute(query, (0,))

    return cursor.fetchall()


def remove_purchase(connection, purchase_id):
    validate_positive_integer(purchase_id, "purchase_id")

    query = "UPDATE purchases SET removed=?, updated_at = CURRENT_TIMESTAMP WHERE id=?"
    values = (1, purchase_id)

    cursor = connection.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise ValueError("purchases not found")


def update_purchase(connection, purchase_id, description, purchase_date, value, installment_count, payment_method_id, category_id, subcategory_id):
    validate_positive_integer(purchase_id, "purchase_id")
    validate_required_string(description, "description")
    purchase_date = validate_and_convert_date(purchase_date)

    validate_positive_integer(value, "value")
    validate_positive_integer(installment_count, "installment_count")
    validate_positive_integer(payment_method_id, "payment_method_id")
    validate_positive_integer(category_id, "category_id")
    validate_positive_integer(subcategory_id, "subcategory_id")

    description = description.strip()
    query = (
        "UPDATE purchases SET description=?, purchase_date=?, value=?, installment_count=?, payment_method_id=?, "
        "category_id=?, subcategory_id=?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
    )
    values = (description, purchase_date, value, installment_count, payment_method_id, category_id, subcategory_id, purchase_id)

    cursor = connection.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise ValueError("purchase not found")

