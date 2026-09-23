from flask import Blueprint, jsonify, render_template, request

from datetime import date, datetime


from app.database.transactions import select_oldest_pending_due_date, select_transactions_details
from app.database.payment_methods import select_payment_methods, select_payment_method_by_id
from app.config import DATABASE_PATH
from app.database.connection import get_connection
from app.services.formatting import format_month, format_account

accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/accounts", methods=["GET"])
def accounts():
    connection = get_connection(DATABASE_PATH)

    try:
        accounts = []
        payment_methods = select_payment_methods(connection)

        for payment_method_id, description, *_ in payment_methods:
            account = {}

            account["payment_method"] = {"id": payment_method_id, "description": description}

            oldest_pending_due_date = select_oldest_pending_due_date(connection, payment_method_id) or date.today().isoformat()
            due_month = format_month(oldest_pending_due_date)

            account["month"] = datetime.strptime(due_month, "%m/%Y").strftime("%Y-%m")

            transactions = select_transactions_details(connection, payment_method_id, due_month, "ASC")

            account = format_account(account, transactions)

            accounts.append(account)

        return render_template("accounts.html", accounts=accounts)

    finally:
        connection.close()



@accounts_bp.route("/accounts/payment-method/<int:payment_method_id>")
def get_account_by_payment_method(payment_method_id):
    month = request.args.get("month")
    due_month = datetime.strptime(month, "%Y-%m").strftime("%m/%Y")

    connection = get_connection(DATABASE_PATH)

    try:
        transactions = select_transactions_details(connection, payment_method_id, due_month, "ASC")

        payment_method = select_payment_method_by_id(connection, payment_method_id)

        account = {
            "payment_method": {"id": payment_method_id, "description": payment_method["description"]},
            "month": month
        }

        account = format_account(account, transactions)

        return jsonify(account)

    finally:
        connection.close()

