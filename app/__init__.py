from flask import Flask

from app.routes.index import index_bp
from app.config import DATABASE_PATH
from app.database.connection import get_connection, create_tables

def create_app():
    app = Flask(__name__)
    app.register_blueprint(index_bp)

    connection = get_connection(DATABASE_PATH)

    try:
        create_tables(connection)
    finally:
        connection.close()

    return app
