import re

from flask import Blueprint, render_template, request, redirect, url_for

from app.config import ITEMS_PER_PAGE, DATABASE_PATH
from app.database.people import select_people, count_people, insert_person, update_person, remove_person
from app.database.payment_methods import count_payment_methods, select_payment_methods, insert_payment_method, update_payment_method, remove_payment_method
from app.database.connection import get_connection


index_bp = Blueprint("index", __name__)


@index_bp.route("/")
def index():
    return render_template("purchases.html")


@index_bp.route("/purchases")
def purchases():
    return render_template("purchases.html")


@index_bp.route("/payment-methods", methods=["GET"])
def payment_methods():
    connection = get_connection(DATABASE_PATH)

    try:
        page = request.args.get("page", 1, type=int)
        search = request.args.get("search")

        if search is not None:
            search = search.strip()

        if page < 1 or ( "search" in request.args and not search):
            return redirect(url_for("index.payment_methods", page=1))

        total_payment_methods = count_payment_methods(connection, search)
        total_pages = max(1, (total_payment_methods + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)

        if page > total_pages:
            return redirect(url_for("index.payment_methods", page=total_pages))

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


@index_bp.route("/payment-methods", methods=["POST"])
def create_payment_method():
    connection = get_connection(DATABASE_PATH)

    try:
        description = request.form.get("description")
        payment_type = request.form.get("payment_type", type=int)
        closing_day = request.form.get("closing_day", type=int)
        due_day = request.form.get("due_day", type=int)
        insert_payment_method(connection, description, payment_type, closing_day, due_day)
    finally:
        connection.close()

    return redirect(url_for("index.payment_methods", page=1))


@index_bp.route("/payment-methods/<int:payment_method_id>/edit", methods=["POST"])
def update_payment_method_route(payment_method_id):
    connection = get_connection(DATABASE_PATH)

    try:
        description = request.form.get("description")
        payment_type = request.form.get("payment_type", type=int)
        closing_day = request.form.get("closing_day", type=int)
        due_day = request.form.get("due_day", type=int)

        update_payment_method(connection, payment_method_id, description, payment_type, closing_day, due_day)
    finally:
        connection.close()

    return redirect(url_for("index.payment_methods", page=1))


@index_bp.route("/payment-methods/<int:payment_method_id>/remove", methods=["POST"])
def remove_payment_method_route(payment_method_id):
    connection = get_connection(DATABASE_PATH)

    try:
        remove_payment_method(connection, payment_method_id)
    finally:
        connection.close()

    return redirect(url_for("index.payment_methods", page=1))


@index_bp.route("/transactions")
def transactions():
    return render_template("transactions.html")


@index_bp.route("/people", methods=["GET"])
def people():
    connection = get_connection(DATABASE_PATH)

    try:
        page = request.args.get("page", 1, type=int)
        search = request.args.get("search")

        if search is not None:
            search = search.strip()

        if page < 1 or ( "search" in request.args and not search):
            return redirect(url_for("index.people", page=1))

        total_people = count_people(connection, search)
        total_pages = max(1, (total_people + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)

        if page > total_pages:
            return redirect(url_for("index.people", page=total_pages))

        people = select_people(connection, page, ITEMS_PER_PAGE, search)
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE

        return render_template(
            "people.html",
            people=people,
            search=search,
            page=page,
            per_page=ITEMS_PER_PAGE,
            total_people=total_people,
            total_pages=total_pages,
            start=start,
            end=min(end, total_people)
        )
    finally:
        connection.close()


@index_bp.route("/people", methods=["POST"])
def create_person():
    connection = get_connection(DATABASE_PATH)

    try:
        phone = re.sub(r"\D", "", request.form["phone"])
        insert_person(connection, request.form["name"], request.form["email"], phone)
    finally:
        connection.close()

    return redirect(url_for("index.people", page=1))


@index_bp.route("/people/<int:person_id>/edit", methods=["POST"])
def update_person_route(person_id):
    connection = get_connection(DATABASE_PATH)

    try:
        phone = re.sub(r"\D", "", request.form["phone"])
        update_person(connection, person_id, request.form["name"], request.form["email"], phone)
    finally:
        connection.close()

    return redirect(url_for("index.people", page=1))


@index_bp.route("/people/<int:person_id>/remove", methods=["POST"])
def remove_person_route(person_id):
    connection = get_connection(DATABASE_PATH)

    try:
        remove_person(connection, person_id)
    finally:
        connection.close()

    return redirect(url_for("index.people", page=1))



