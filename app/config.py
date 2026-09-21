import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if os.getenv("APP_ENV") == "production":
    DATABASE_PATH = BASE_DIR / "instance_prod" / "database.db"
else:
    DATABASE_PATH = BASE_DIR / "instance" / "database.db"

ITEMS_PER_PAGE = 6

CASH = 1
CREDIT = 2

CATEGORIES = {
    1: "Alimentação",
    2: "Animais",
    3: "Assinaturas",
    4: "Casa",
    5: "Educação",
    6: "Transporte",
    7: "Outros",
    8: "Saúde",
}

SUBCATEGORIES = {
    1: "Academia",
    2: "Água",
    3: "Aluguel",
    4: "Anuidade",
    5: "Cachorro",
    6: "Carne",
    7: "Conta de Água",
    8: "Dentista",
    9: "Energia",
    10: "Ext. Animais",
    11: "Faculdade",
    12: "Faculdade (L)",
    13: "Feira",
    14: "Festividades",
    15: "Frutas",
    16: "Gasolina",
    17: "Gatos",
    18: "HBO",
    19: "Internet",
    20: "Lanches",
    21: "Luiza",
    22: "Manutenção",
    23: "Moto",
    24: "Netflix",
    25: "Outros",
    26: "Seguro Moto",
    27: "Verdura",
    28: "Vivo",
}
