import sqlite3

def get_connection(database_path):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        removed INTEGER NOT NULL DEFAULT 0
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS payment_methods (
        id INTEGER PRIMARY KEY,
        description TEXT NOT NULL,
        payment_type INTEGER NOT NULL,
        closing_day INTEGER,
        due_day INTEGER,
        removed INTEGER NOT NULL DEFAULT 0
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY,
        description TEXT NOT NULL,
        purchase_date DATE NOT NULL,
        value INTEGER NOT NULL,
        installment_count INTEGER NOT NULL,
        payment_method_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        subcategory_id INTEGER NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP,
        removed INTEGER NOT NULL DEFAULT 0,

        FOREIGN KEY (payment_method_id) REFERENCES payment_methods (id)
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        purchase_id INTEGER NOT NULL,
        person_id INTEGER NOT NULL,
        installment INTEGER NOT NULL,
        value INTEGER NOT NULL,
        due_date DATE NOT NULL,
        payment_date DATE,
        status INTEGER NOT NULL DEFAULT 0,
        removed INTEGER NOT NULL DEFAULT 0,

        FOREIGN KEY (purchase_id) REFERENCES purchases (id),
        FOREIGN KEY (person_id) REFERENCES people (id)
    )""")



