from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from app.config import DATABASE_PATH, CATEGORIES, SUBCATEGORIES
from app.database.connection import get_connection
from app.database.people import select_people
from app.database.payment_methods import select_payment_methods
from app.database.purchases import select_purchases_for_management, select_purchase_by_id, insert_purchase, remove_purchase, update_purchase
from app.database.transactions import insert_transaction, select_transactions_by_purchase_id, remove_transaction, update_transaction
from app.services.formatting import format_purchases
from app.services.validation import currency_to_cents, html_date_to_br_date


purchases_bp = Blueprint("purchases", __name__)


@purchases_bp.route("/purchases", methods=["GET"])
def purchases():
    connection = get_connection(DATABASE_PATH)

    try:
        purchases = select_purchases_for_management(connection)
        purchases = format_purchases(purchases)

        people = select_people(connection)
        payment_methods = select_payment_methods(connection)

        return render_template(
            "purchases.html",
            purchases=purchases,
            categories=CATEGORIES,
            subcategories=SUBCATEGORIES,
            people=people,
            payment_methods=payment_methods
        )

    finally:
        connection.close()


@purchases_bp.route("/purchases", methods=["POST"])
def create_purchase():
    connection = get_connection(DATABASE_PATH)

    try:
        purchase_id = insert_purchase(
            connection,
            request.form["description"],
            html_date_to_br_date(request.form["purchase_date"]),
            currency_to_cents(request.form["value"]),
            int(request.form["installment_count"]),
            int(request.form["payment_method_id"]),
            int(request.form["category_id"]),
            int(request.form["subcategory_id"])
        )

        installment_numbers = request.form.getlist("installment_number")
        person_ids = request.form.getlist("person_id")
        amounts = request.form.getlist("amount")
        due_dates = request.form.getlist("due_date")

        for installment_number, person_id, amount, due_date in zip(installment_numbers, person_ids, amounts, due_dates):
            insert_transaction(connection, purchase_id, int(person_id), int(installment_number), currency_to_cents(amount), html_date_to_br_date(due_date), 0)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("purchases.purchases"))


@purchases_bp.route("/purchases/<int:purchase_id>/edit-data", methods=["GET"])
def purchase_edit_data(purchase_id):
    connection = get_connection(DATABASE_PATH)

    try:
        purchase = select_purchase_by_id(connection, purchase_id)

        if purchase is None:
            return jsonify({"error": "Compra não encontrada"}), 404

        transactions = select_transactions_by_purchase_id(connection, purchase_id)

        return jsonify({
            "purchase": dict(purchase),
            "transactions": [
                dict(transaction)
                for transaction in transactions
            ]
        })

    finally:
        connection.close()


@purchases_bp.route("/purchases/<int:purchase_id>/remove", methods=["POST"])
def remove_purchase_route(purchase_id):
    connection = get_connection(DATABASE_PATH)

    try:
        transactions = select_transactions_by_purchase_id(connection, purchase_id)

        for transaction in transactions:
            remove_transaction(connection, transaction["id"])

        remove_purchase(connection, purchase_id)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("purchases.purchases"))


@purchases_bp.route("/purchases/<int:purchase_id>/edit", methods=["POST"])
def update_purchase_route(purchase_id):
    connection = get_connection(DATABASE_PATH)

    try:
        update_purchase(
            connection,
            purchase_id,
            request.form["description"],
            html_date_to_br_date(request.form["purchase_date"]),
            currency_to_cents(request.form["value"]),
            int(request.form["installment_count"]),
            int(request.form["payment_method_id"]),
            int(request.form["category_id"]),
            int(request.form["subcategory_id"])
        )

        existing_transactions = select_transactions_by_purchase_id(connection, purchase_id)

        existing_ids = {transaction["id"] for transaction in existing_transactions}

        transaction_ids = request.form.getlist("transaction_id")
        installment_numbers = request.form.getlist("installment_number")
        person_ids = request.form.getlist("person_id")
        amounts = request.form.getlist("amount")
        due_dates = request.form.getlist("due_date")

        received_ids = set()

        for transaction_id, installment_number, person_id, amount, due_date in zip(transaction_ids, installment_numbers, person_ids, amounts, due_dates):
            if transaction_id:
                transaction_id = int(transaction_id)
                received_ids.add(transaction_id)

                update_transaction(connection, transaction_id, purchase_id, int(person_id), int(installment_number), currency_to_cents(amount), html_date_to_br_date(due_date))

            else:
                insert_transaction(connection, purchase_id, int(person_id), int(installment_number), currency_to_cents(amount), html_date_to_br_date(due_date), 0)

        removed_ids = existing_ids - received_ids

        for transaction_id in removed_ids:
            remove_transaction(connection, transaction_id)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("purchases.purchases"))


