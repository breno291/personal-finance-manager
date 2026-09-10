import sqlite3

from app.services.validation import validate_required_string, validate_positive_integer, validate_email, validate_phone

def insert_person(connection, name, email, phone):
    validate_required_string(name, "name")
    validate_email(email)
    validate_phone(phone)

    name = name.strip()
    email = email.strip()
    phone = phone.strip()

    try:
        query = "INSERT INTO people (name, email, phone) VALUES (?, ?, ?)"
        values = (name, email, phone)

        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()

        return cursor.lastrowid

    except sqlite3.Error:
        connection.rollback()
        raise


def select_person_by_id(connection, person_id):
    validate_positive_integer(person_id, "person_id")

    query = "SELECT id, name, email, phone FROM people WHERE id = ? AND removed = ?"
    cursor = connection.cursor()
    cursor.execute(query, (person_id, 0))

    return cursor.fetchone()


def select_people(connection, page=None, total_number_of_items=None, search=None):
    query = "SELECT id, name, email, phone FROM people WHERE removed = ?"
    values = []
    values.append(0)

    if search is not None:
        query += " AND name LIKE ?"
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


def count_people(connection, search=None):
    query = "SELECT COUNT(id) FROM people WHERE removed = ?"
    values = []
    values.append(0)

    if search is not None:
        query += " AND name LIKE ?"
        values.append(f"%{search}%")

    cursor = connection.cursor()
    cursor.execute(query, values)

    return cursor.fetchone()[0]


def update_person(connection, person_id, name, email, phone):
    validate_positive_integer(person_id, "person_id")
    validate_required_string(name, "name")
    validate_email(email)
    validate_phone(phone)

    name = name.strip()
    email = email.strip()
    phone = phone.strip()

    try:
        query = "UPDATE people SET name=?, email=?, phone=? WHERE id=?"
        values = (name, email, phone, person_id)

        cursor = connection.cursor()
        cursor.execute(query, values)

        if cursor.rowcount == 0:
            raise ValueError("person not found")

        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        raise


def remove_person(connection, person_id):
    validate_positive_integer(person_id, "person_id")

    try:
        query = "UPDATE people SET removed=? WHERE id=?"
        values = (1, person_id)

        cursor = connection.cursor()
        cursor.execute(query, values)
        if cursor.rowcount == 0:
            raise ValueError("person not found")

        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        raise




