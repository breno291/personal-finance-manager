from app.routes.index import index_bp
from app.routes.people import people_bp
from app.routes.payment_methods import payment_methods_bp
from app.routes.purchases import purchases_bp
from app.routes.transactions import transactions_bp


def register_blueprints(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(people_bp)
    app.register_blueprint(payment_methods_bp)
    app.register_blueprint(purchases_bp)
    app.register_blueprint(transactions_bp)

