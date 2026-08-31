import sqlite3

from app.services.validation import validate_required_string, validate_positive_integer

def insert_person(connection, name):
    validate_required_string(name, "name")
    name = name.strip()

    try:
        query = "INSERT INTO people (name) VALUES (?)"
        values = (name,)

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


