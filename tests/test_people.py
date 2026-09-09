import pytest

from app.database.people import *

def test_insert_person(connection):
    person_id = insert_person(connection,"    Breno    ","    breno@email.com    ","    81999999999    ")
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


def test_select_person_by_id_with_removed_person(connection):
    person_id = insert_person(connection, "Gabi", "gabi@email.com", "81988888888")

    cursor = connection.cursor()
    cursor.execute("UPDATE people SET removed = 1 WHERE id = ?", (person_id,))
    connection.commit()

    selected_person = select_person_by_id(connection, person_id)

    assert selected_person is None


def test_select_people(connection):
    insert_person(connection, "Breno", "breno@gmail.com", "81982474242")
    insert_person(connection, "Luh", "luh@gmail.com", "81982474244")
    insert_person(connection, "Ana", "ana@gmail.com", "81982474223")

    people = select_people(connection)

    assert len(people) == 3
    assert people[0][1] == "Breno"
    assert people[1][2] == "luh@gmail.com"
    assert people[2][0] == 3


def test_select_people_excludes_removed(connection):
    insert_person(connection, "Breno", "breno@gmail.com", "81982474242")
    person_id = insert_person(connection, "Gabi", "gabi@email.com", "81988888888")
    insert_person(connection, "Luh", "luh@gmail.com", "81982474244")

    cursor = connection.cursor()
    cursor.execute("UPDATE people SET removed = 1 WHERE id = ?", (person_id,))
    connection.commit()

    people = select_people(connection)

    assert len(people) == 2
    assert people[0][1] == "Breno"
    assert people[1][2] == "luh@gmail.com"
    assert people[1][0] == 3


def test_select_people_empty(connection):
    people = select_people(connection)

    assert len(people) == 0


def test_select_people_with_pagination(connection):
    page = 1
    total_number_of_items = 6
    for i in range(10): 
        insert_person(connection, f"test_{i}", f"test_{i}@gmail.com", f"8198242424{i}")

    people = select_people(connection, page, total_number_of_items)
    assert len(people) == total_number_of_items
    assert people[0][1] == "test_9"
    assert people[1][1] == "test_8"
    assert people[2][1] == "test_7"
    assert people[3][1] == "test_6"
    assert people[4][1] == "test_5"
    assert people[5][1] == "test_4"


    page = 2
    people_dois = select_people(connection, page, total_number_of_items)
    assert len(people_dois) == 4
    assert people_dois[0][1] == "test_3"
    assert people_dois[1][1] == "test_2"
    assert people_dois[2][1] == "test_1"
    assert people_dois[3][1] == "test_0"


def test_select_people_with_invalid_page(connection):
    with pytest.raises(ValueError):
        select_people(connection, 0, 6)

    with pytest.raises(ValueError):
        select_people(connection, -1, 6)

    with pytest.raises(ValueError):
        select_people(connection, "1", 6)

    with pytest.raises(ValueError):
        select_people(connection, True, 6)


def test_select_people_with_invalid_total_number_of_items(connection):
    with pytest.raises(ValueError):
        select_people(connection, 1, 0)

    with pytest.raises(ValueError):
        select_people(connection, 1, -1)

    with pytest.raises(ValueError):
        select_people(connection, 1, "6")

    with pytest.raises(ValueError):
        select_people(connection, 1, True)


def test_count_people(connection):
    assert count_people(connection) == 0

    for i in range(3):
        insert_person(connection, f"test_{i}", f"test_{i}@gmail.com", f"8198242424{i}")

    assert count_people(connection) == 3

    person_id = insert_person(connection, "Gabi", "gabi@email.com", "81988888888")
    assert count_people(connection) == 4

    cursor = connection.cursor()
    cursor.execute("UPDATE people SET removed = 1 WHERE id = ?", (person_id,))
    connection.commit()
    assert count_people(connection) == 3


def test_count_people_with_search(connection):
    insert_person(connection, "Luciana", "luciana@email.com", "81982474242")
    insert_person(connection, "Briana", "briana@email.com", "81982474243")
    insert_person(connection, "Breno", "breno@email.com", "81982474244")

    assert count_people(connection, search="ana") == 2
    assert count_people(connection, search="Breno") == 1
    assert count_people(connection, search="Gabi") == 0


def test_select_people_with_search(connection):
    insert_person(connection, "Breno", "breno@email.com", "81982474242")
    insert_person(connection, "Gabi", "gabi@email.com", "81988888888")
    person_id = insert_person(connection, "Luciana", "luciana@email.com", "81982474242")
    insert_person(connection, "Briana", "briana@email.com", "81982474242")

    selected_person = select_people(connection, search="Gabi")
    assert selected_person[0][1] == "Gabi"
    assert selected_person[0][2] == "gabi@email.com"
    assert selected_person[0][3] == "81988888888"


    selected_person = select_people(connection, search="ana")
    assert selected_person[0][1] == "Luciana"
    assert selected_person[0][2] == "luciana@email.com"
    assert selected_person[0][3] == "81982474242"

    assert selected_person[1][1] == "Briana"
    assert selected_person[1][2] == "briana@email.com"
    assert selected_person[1][3] == "81982474242"


    cursor = connection.cursor()
    cursor.execute("UPDATE people SET removed = 1 WHERE id = ?", (person_id,))
    connection.commit()
    selected_person = select_people(connection, search="ana")
    assert selected_person[0][1] == "Briana"
    assert selected_person[0][2] == "briana@email.com"
    assert selected_person[0][3] == "81982474242"


def test_select_people_with_search_and_pagination(connection):
    for i in range(10):
        insert_person(connection, f"Teste {i}", f"teste{i}@email.com", f"8198242424{i}")

    insert_person(connection, "Breno", "breno@email.com", "81982474242")

    people = select_people(connection, page=1, total_number_of_items=6, search="Teste")

    assert len(people) == 6
    assert people[0][1] == "Teste 9"
    assert people[5][1] == "Teste 4"

    people = select_people(connection, page=2, total_number_of_items=6, search="Teste")

    assert len(people) == 4
    assert people[0][1] == "Teste 3"
    assert people[3][1] == "Teste 0"


def test_update_person(connection):
    person_id = insert_person(connection, "Breno", "breno@email.com", "81982474242")
    update_person(connection, person_id, "Luciana", "luh@email.com", "81982889567")
    person = select_person_by_id(connection, person_id)

    assert person[1] == "Luciana"
    assert person[2] == "luh@email.com"
    assert person[3] == "81982889567"


def test_update_person_with_nonexistent_id(connection):
    with pytest.raises(ValueError):
        update_person(connection, 9999, "Teste", "teste@email.com", "81982889567")


def test_update_person_with_invalid_id(connection):
    with pytest.raises(ValueError):
        update_person(connection, 0, "Teste", "teste@email.com", "81982889567")


def test_update_person_with_invalid_email(connection):
    person_id = insert_person(connection, "Breno", "breno@email.com", "81982474242")

    with pytest.raises(ValueError):
        update_person(connection, person_id, "Breno", "email-invalido", "81982474242")


def test_remove_person(connection):
    person_id = insert_person(connection, "teste", "teste@email.com", "89182474222")
    remove_person(connection, person_id)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM people WHERE id = ?", (person_id,))
    person = cursor.fetchone()

    assert person[4] == 1


def test_remove_person_with_nonexistent_id(connection):
    with pytest.raises(ValueError):
        remove_person(connection, 9999)


def test_remove_person_with_invalid_id(connection):
    with pytest.raises(ValueError):
        remove_person(connection, -1)


