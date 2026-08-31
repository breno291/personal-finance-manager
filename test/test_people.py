import pytest

from app.database.people import *

def test_insert_person(connection):
    person_id = insert_person(connection, "    Breno    ")
    assert person_id is not None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM people WHERE id = ?", (person_id,))
    person = cursor.fetchone()

    assert person[0] == person_id
    assert person[1] == "Breno"
    assert person[2] == 0


def test_insert_person_without_name(connection):
    with pytest.raises(ValueError):
        insert_person(connection, None)

    with pytest.raises(ValueError):
        insert_person(connection, "   ")

    with pytest.raises(ValueError):
        insert_person(connection, 123)

def test_select_person_by_id(connection):
    person_id = insert_person(connection, "Gabi")
    selected_person = select_person_by_id(connection, person_id)

    assert selected_person[0] == person_id
    assert selected_person[1] == "Gabi"
    assert selected_person[2] == 0


def test_select_person_by_id_with_invalid_id(connection):
    with pytest.raises(ValueError):
        select_person_by_id(connection, None)

    with pytest.raises(ValueError):
        select_person_by_id(connection, True)

    with pytest.raises(ValueError):
        select_person_by_id(connection, "1")

    with pytest.raises(ValueError):
        select_person_by_id(connection, 0)

    with pytest.raises(ValueError):
        select_person_by_id(connection, -1)


def test_select_person_by_id_with_nonexistent_id(connection):
    assert select_person_by_id(connection, 2) is None




