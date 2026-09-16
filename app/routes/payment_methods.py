from flask import Blueprint, redirect, render_template, request, url_for

from app.config import DATABASE_PATH, ITEMS_PER_PAGE
from app.database.connection import get_connection
from app.database.payment_methods import count_payment_methods, select_payment_methods, insert_payment_method, update_payment_method, remove_payment_method


payment_methods_bp = Blueprint("payment_methods", __name__)


@payment_methods_bp.route("/payment-methods", methods=["GET"])
def payment_methods():
    connection = get_connection(DATABASE_PATH)

    try:
        page = request.args.get("page", 1, type=int)
        search = request.args.get("search")

        if search is not None:
            search = search.strip()

        if page < 1 or ("search" in request.args and not search):
            return redirect(url_for("payment_methods.payment_methods", page=1))

        total_payment_methods = count_payment_methods(connection, search)
        total_pages = max(1, (total_payment_methods + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)

        if page > total_pages:
            return redirect(
                url_for("payment_methods.payment_methods", page=total_pages)
            )

        payment_methods = select_payment_methods(connection, page, ITEMS_PER_PAGE, search)

        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE

        return render_template(
            "payment_methods.html",
            payment_methods=payment_methods,
            search=search,
            page=page,
            per_page=ITEMS_PER_PAGE,
            total_payment_methods=total_payment_methods,
            total_pages=total_pages,
            start=start,
            end=min(end, total_payment_methods)
        )

    finally:
        connection.close()


@payment_methods_bp.route("/payment-methods", methods=["POST"])
def create_payment_method():
    connection = get_connection(DATABASE_PATH)

    try:
        description = request.form.get("description")
        payment_type = request.form.get("payment_type", type=int)
        closing_day = request.form.get("closing_day", type=int)
        due_day = request.form.get("due_day", type=int)

        insert_payment_method(connection, description, payment_type, closing_day, due_day)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("payment_methods.payment_methods", page=1))


@payment_methods_bp.route("/payment-methods/<int:payment_method_id>/edit", methods=["POST"])
def update_payment_method_route(payment_method_id):
    connection = get_connection(DATABASE_PATH)

    try:
        description = request.form.get("description")
        payment_type = request.form.get("payment_type", type=int)
        closing_day = request.form.get("closing_day", type=int)
        due_day = request.form.get("due_day", type=int)

        update_payment_method(connection, payment_method_id, description, payment_type, closing_day, due_day)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("payment_methods.payment_methods", page=1))


@payment_methods_bp.route("/payment-methods/<int:payment_method_id>/remove", methods=["POST"])
def remove_payment_method_route(payment_method_id):
    connection = get_connection(DATABASE_PATH)

    try:
        remove_payment_method(connection, payment_method_id)
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("payment_methods.payment_methods", page=1))


