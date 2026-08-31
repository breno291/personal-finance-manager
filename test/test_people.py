import pytest

from app.database.people import *

def test_insert_person(connection):
    person_id = insert_person(
        connection,
        "    Breno    ",
        "    breno@email.com    ",
        "    81999999999    "
    )
    assert person_id is not None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM people WHERE id = ?", (person_id,))
    person = cursor.fetchone()

    assert person[0] == person_id
    assert person[1] == "Breno"
    assert person[2] == "breno@email.com"
    assert person[3] == "81999999999"
    assert person[4] == 0


def test_insert_person_without_name(connection):
    with pytest.raises(ValueError):
        insert_person(connection, None, "breno@email.com", "81999999999")

    with pytest.raises(ValueError):
        insert_person(connection, "   ", "breno@email.com", "81999999999")

    with pytest.raises(ValueError):
        insert_person(connection, 123, "breno@email.com", "81999999999")


def test_select_person_by_id(connection):
    person_id = insert_person(connection, "Gabi", "gabi@email.com", "81988888888")
    selected_person = select_person_by_id(connection, person_id)

    assert selected_person[0] == person_id
    assert selected_person[1] == "Gabi"
    assert selected_person[2] == "gabi@email.com"
    assert selected_person[3] == "81988888888"
    assert selected_person[4] == 0


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


def test_insert_person_without_email(connection):
    with pytest.raises(ValueError):
        insert_person(connection, "Breno", None, "81999999999")

    with pytest.raises(ValueError):
        insert_person(connection, "Breno", "   ", "81999999999")

    with pytest.raises(ValueError):
        insert_person(connection, "Breno", 123, "81999999999")


def test_insert_person_with_invalid_email(connection):
    with pytest.raises(ValueError):
        insert_person(connection, "Breno", "brenoemail.com", "81999999999")

    with pytest.raises(ValueError):
        insert_person(connection, "Breno", "breno@", "81999999999")


def test_insert_person_without_phone(connection):
    with pytest.raises(ValueError):
        insert_person(connection, "Breno", "breno@email.com", None)

    with pytest.raises(ValueError):
        insert_person(connection, "Breno", "breno@email.com", "   ")

    with pytest.raises(ValueError):
        insert_person(connection, "Breno", "breno@email.com", 123)


def test_insert_person_with_invalid_phone(connection):
    with pytest.raises(ValueError):
        insert_person(connection, "Breno", "breno@email.com", "819999")

    with pytest.raises(ValueError):
        insert_person(connection, "Breno", "breno@email.com", "819999999999")

    with pytest.raises(ValueError):
        insert_person(connection, "Breno", "breno@email.com", "81999abc999")


