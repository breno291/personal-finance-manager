import pytest
from app.database.connection import get_connection, create_tables

@pytest.fixture
def connection(tmp_path):
    database_path = tmp_path / "finance.db"
    connection = get_connection(database_path)
    create_tables(connection)

    yield connection

    connection.close()