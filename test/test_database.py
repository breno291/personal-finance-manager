from pathlib import Path

from app.database.connection import get_connection
from app.database.connection import create_tables

def test_database_created(tmp_path):
    database_path = tmp_path / "finance.db"

    connection = get_connection(database_path)
    assert Path(database_path).exists()
    assert connection is not None

    cursor = connection.cursor()
    cursor.execute("CREATE TABLE teste (id INTEGER PRIMARY KEY)")
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'teste'")
    assert cursor.fetchone() is not None

    connection.close()


def test_create_tables(tmp_path):
    database_path = tmp_path / "finance.db"
    connection = get_connection(database_path)

    create_tables(connection)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='people'")
    assert cursor.fetchone() is not None
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='payment_methods'")
    assert cursor.fetchone() is not None
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='purchases'")
    assert cursor.fetchone() is not None
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
    assert cursor.fetchone() is not None

    cursor.execute("PRAGMA table_info(people)")
    assert [col[1] for col in cursor.fetchall()] == [
        "id",
        "name",
        "removed"
    ]

    cursor.execute("PRAGMA table_info(payment_methods)")
    assert [col[1] for col in cursor.fetchall()] == [
        "id",
        "description",
        "payment_type",
        "closing_day",
        "due_day",
        "removed"
    ]

    cursor.execute("PRAGMA table_info(purchases)")
    assert [col[1] for col in cursor.fetchall()] == [
        "id",
        "description",
        "purchase_date",
        "value",
        "installment_count",
        "payment_method_id",
        "category_id",
        "subcategory_id",
        "created_at",
        "updated_at",
        "removed"
    ]

    cursor.execute("PRAGMA table_info(transactions)")
    assert [col[1] for col in cursor.fetchall()] == [
        "id",
        "purchase_id",
        "person_id",
        "installment",
        "value",
        "due_date",
        "payment_date",
        "status",
        "removed"
    ]

    connection.close()


def test_table_constraints(connection):
    cursor = connection.cursor()

    # People types and constraints
    cursor.execute("PRAGMA table_info(people)")
    columns = cursor.fetchall()

    assert columns[0][2] == "INTEGER"
    assert columns[1][2] == "TEXT"
    assert columns[2][2] == "INTEGER"

    assert columns[1][3] == 1  # name NOT NULL
    assert columns[2][3] == 1  # removed NOT NULL

    assert columns[2][4] == "0"  # removed DEFAULT 0

    # Payment method types and constraints
    cursor.execute("PRAGMA table_info(payment_methods)")
    columns = cursor.fetchall()

    assert columns[0][2] == "INTEGER"
    assert columns[1][2] == "TEXT"
    assert columns[2][2] == "INTEGER"
    assert columns[3][2] == "INTEGER"
    assert columns[4][2] == "INTEGER"
    assert columns[5][2] == "INTEGER"

    assert columns[1][3] == 1  # description NOT NULL
    assert columns[2][3] == 1  # payment_type NOT NULL
    assert columns[3][3] == 0  # closing_day can be NULL
    assert columns[4][3] == 0  # due_day can be NULL
    assert columns[5][3] == 1  # removed NOT NULL

    assert columns[5][4] == "0"  # removed DEFAULT 0

    # Purchase types and constraints
    cursor.execute("PRAGMA table_info(purchases)")
    columns = cursor.fetchall()

    assert columns[0][2] == "INTEGER"
    assert columns[1][2] == "TEXT"
    assert columns[2][2] == "DATE"
    assert columns[3][2] == "INTEGER"
    assert columns[4][2] == "INTEGER"
    assert columns[5][2] == "INTEGER"
    assert columns[6][2] == "INTEGER"
    assert columns[7][2] == "INTEGER"
    assert columns[8][2] == "TIMESTAMP"
    assert columns[9][2] == "TIMESTAMP"
    assert columns[10][2] == "INTEGER"

    assert columns[1][3] == 1  # description NOT NULL
    assert columns[2][3] == 1  # purchase_date NOT NULL
    assert columns[3][3] == 1  # value NOT NULL
    assert columns[4][3] == 1  # installment_count NOT NULL
    assert columns[5][3] == 1  # payment_method_id NOT NULL
    assert columns[6][3] == 1  # category_id NOT NULL
    assert columns[7][3] == 1  # subcategory_id NOT NULL
    assert columns[8][3] == 1  # created_at NOT NULL
    assert columns[9][3] == 0  # updated_at can be NULL
    assert columns[10][3] == 1  # removed NOT NULL

    assert columns[8][4] == "CURRENT_TIMESTAMP"  # created_at DEFAULT
    assert columns[10][4] == "0"  # removed DEFAULT 0

    # Transaction types and constraints
    cursor.execute("PRAGMA table_info(transactions)")
    columns = cursor.fetchall()

    assert columns[0][2] == "INTEGER"
    assert columns[1][2] == "INTEGER"
    assert columns[2][2] == "INTEGER"
    assert columns[3][2] == "INTEGER"
    assert columns[4][2] == "INTEGER"
    assert columns[5][2] == "DATE"
    assert columns[6][2] == "DATE"
    assert columns[7][2] == "INTEGER"
    assert columns[8][2] == "INTEGER"

    assert columns[1][3] == 1  # purchase_id NOT NULL
    assert columns[2][3] == 1  # person_id NOT NULL
    assert columns[3][3] == 1  # installment NOT NULL
    assert columns[4][3] == 1  # value NOT NULL
    assert columns[5][3] == 1  # due_date NOT NULL
    assert columns[6][3] == 0  # payment_date can be NULL
    assert columns[7][3] == 1  # status NOT NULL
    assert columns[8][3] == 1  # removed NOT NULL

    assert columns[7][4] == "0"  # status DEFAULT 0
    assert columns[8][4] == "0"  # removed DEFAULT 0


def test_foreign_keys(connection):
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_key_list(purchases)")
    foreign_keys = cursor.fetchall()

    assert any(fk[2] == "payment_methods" for fk in foreign_keys)

    cursor.execute("PRAGMA foreign_key_list(transactions)")
    foreign_keys = cursor.fetchall()

    assert any(fk[2] == "purchases" for fk in foreign_keys)
    assert any(fk[2] == "people" for fk in foreign_keys)


def test_foreign_keys_enabled(connection):
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys")

    assert cursor.fetchone()[0] == 1



