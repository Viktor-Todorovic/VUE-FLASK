import os

from flask import Flask
from flask_cors import CORS

from routes.cart import cart_bp
from routes.comments import comments_bp
from routes.orders import orders_bp
from routes.products import products_bp
from routes.sessions import sessions_bp
from routes.users import users_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "RAF2021-2022"
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True

    app.config['UPLOAD_FOLDER'] = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../frontend/src/assets/slike_korisnici")
    )
    app.config['UPLOAD_FOLDER_PROIZVODI'] = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../frontend/src/assets/slike_proizvodi")
    )

    CORS(app, supports_credentials=True)

    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(sessions_bp)

    @app.route('/')
    def index():
        return 'Hello world'

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
