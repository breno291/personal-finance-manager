from datetime import date, datetime
from app.config import CATEGORIES, SUBCATEGORIES

def format_currency(value):
    value_in_reais = value / 100

    return (f"R$ {value_in_reais:,.2f}".replace(",", "_").replace(".", ",").replace("_", "."))


def format_date(value):
    if isinstance(value, (date, datetime)):
        return value.strftime("%d/%m/%Y")

    return datetime.strptime(value, "%Y-%m-%d").strftime("%d/%m/%Y")


def format_datetime(value):
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y %H:%M")

    return datetime.strptime(value,"%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")


def format_purchase(purchase):
    formatted_purchase = dict(purchase)

    formatted_purchase["purchase_date_order"] = purchase["purchase_date"]
    formatted_purchase["purchase_date"] = format_date(purchase["purchase_date"])

    formatted_purchase["created_at_order"] = purchase["created_at"]
    formatted_purchase["created_at"] = format_datetime(purchase["created_at"])

    formatted_purchase["value"] = format_currency(purchase["value"])
    formatted_purchase["category"] = CATEGORIES.get(purchase["category_id"], "Valor Invalido")
    formatted_purchase["subcategory"] = SUBCATEGORIES.get(purchase["subcategory_id"], "Valor Invalido")

    return formatted_purchase


def format_purchases(purchases):
    return [format_purchase(purchase) for purchase in purchases]

