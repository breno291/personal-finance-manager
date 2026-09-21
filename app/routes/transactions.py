from flask import Blueprint, render_template, request

from app.config import DATABASE_PATH
from app.database.connection import get_connection
from app.database.transactions import select_transactions_details, update_transaction_status, select_transaction_by_id
from app.services.formatting import format_transactions, format_datetime

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/transactions")
def transactions():
    connection = get_connection(DATABASE_PATH)

    try:
        transactions = select_transactions_details(connection)
        transactions = format_transactions(transactions)

        return render_template(
            "transactions.html",
            transactions=transactions,
        )

    finally:
        connection.close()


@transactions_bp.route("/transactions/<int:transaction_id>/status", methods=["POST"])
def update_transaction_status_route(transaction_id):
    connection = get_connection(DATABASE_PATH)

    try:
        status = int(request.form["status"])

        update_transaction_status(connection, transaction_id, status)

        connection.commit()

        transaction = select_transaction_by_id(connection, transaction_id)
        payment_date = (format_datetime(transaction["payment_date"]) if transaction["payment_date"] else None)

        return {
            "status": transaction["status"],
            "payment_date": payment_date
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

