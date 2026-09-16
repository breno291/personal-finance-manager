import re

from flask import Blueprint, redirect, render_template, request, url_for

from app.config import DATABASE_PATH, ITEMS_PER_PAGE
from app.database.connection import get_connection
from app.database.people import select_people, count_people, insert_person, update_person, remove_person


people_bp = Blueprint("people", __name__)


@people_bp.route("/people", methods=["GET"])
def people():
    connection = get_connection(DATABASE_PATH)

    try:
        page = request.args.get("page", 1, type=int)
        search = request.args.get("search")

        if search is not None:
            search = search.strip()

        if page < 1 or ("search" in request.args and not search):
            return redirect(url_for("people.people", page=1))

        total_people = count_people(connection, search)
        total_pages = max(1, (total_people + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)

        if page > total_pages:
            return redirect(url_for("people.people", page=total_pages))

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


@people_bp.route("/people", methods=["POST"])
def create_person():
    connection = get_connection(DATABASE_PATH)

    try:
        phone = re.sub(r"\D", "", request.form["phone"])

        insert_person(connection, request.form["name"], request.form["email"], phone)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("people.people", page=1))


@people_bp.route("/people/<int:person_id>/edit", methods=["POST"])
def update_person_route(person_id):
    connection = get_connection(DATABASE_PATH)

    try:
        phone = re.sub(r"\D", "", request.form["phone"])

        update_person(connection, person_id, request.form["name"], request.form["email"], phone)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("people.people", page=1))


@people_bp.route("/people/<int:person_id>/remove", methods=["POST"])
def remove_person_route(person_id):
    connection = get_connection(DATABASE_PATH)

    try:
        remove_person(connection, person_id)
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("people.people", page=1))


