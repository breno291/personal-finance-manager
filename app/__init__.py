from flask import Flask

from app.routes import register_blueprints
from app.config import DATABASE_PATH
from app.database.connection import get_connection, create_tables


def create_app():
    app = Flask(__name__)

    register_blueprints(app)

    connection = get_connection(DATABASE_PATH)

    try:
        create_tables(connection)
    finally:
        connection.close()

    return app