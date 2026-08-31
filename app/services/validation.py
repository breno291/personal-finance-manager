import re

from datetime import datetime

def validate_required_string(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty")


def validate_positive_integer(value, field_name):
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"The {field_name} must be a positive integer.")


def validate_payment_days(closing_day, due_day):
    if due_day is None and closing_day is None:
        return

    if due_day is None or closing_day is None:
        raise ValueError("closing_day and due_day must be provided together")

    validate_positive_integer(due_day, "due_day")
    validate_positive_integer(closing_day, "closing_day")

    if due_day > 31:
        raise ValueError("The due_day must be between 1 and 31.")

    if closing_day > 31:
        raise ValueError("The closing_day must be between 1 and 31.")

    if due_day == closing_day:
        raise ValueError("The due_day cannot be the same as the closing_day.")


def validate_and_convert_date(date_value):
    validate_required_string(date_value, "date_value")
    try:
        return datetime.strptime(date_value, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("The date_value must be in DD/MM/YYYY format.")


def validate_transaction_status(status):
    if not isinstance(status, int) or isinstance(status, bool):
        raise ValueError("The status must be an integer.")

    if status < 0 or status > 2:
        raise ValueError("The status must be between 0 and 2.")


def validate_email(email):
    validate_required_string(email, "email")

    email = email.strip()

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(pattern, email):
        raise ValueError("email must be a valid email")


def validate_phone(phone):
    validate_required_string(phone, "phone")

    phone = phone.strip()

    if not phone.isdigit():
        raise ValueError("phone must contain only numbers")

    if len(phone) not in (10, 11):
        raise ValueError("phone must have 10 or 11 digits")



