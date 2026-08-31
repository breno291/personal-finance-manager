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

    query = "SELECT * FROM people WHERE id = ?"
    cursor = connection.cursor()
    cursor.execute(query, (person_id,))

    return cursor.fetchone()


