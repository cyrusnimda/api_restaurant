from flask import Flask, jsonify
from api.models import db
from api.models_schemas import ma
from api.config import DevelopmentConfig, ProductionConfig
import os
from flask_cors import CORS
from api.routes.restaurant import router as restaurant_router
from api.routes.base import router as main_router
from api.routes.booking import router as booking_router
from api.routes.user import router as user_router
from api.routes.auth import router as auth_router
from api.routes.table import router as table_router


def create_app(env_object = None):
    # Check enviroment value
    if env_object is None:
        enviroment_mode = os.getenv('SERVER_ENV', 'Development')
        env_object = globals()[enviroment_mode + "Config"]


    app = Flask(__name__)
    CORS(app)

    app.config.from_object(env_object)

    # Load database model
    db.init_app(app)
    ma.init_app(app)


    # Add all endpoints form routes
    app.register_blueprint(main_router)
    app.register_blueprint(restaurant_router)
    app.register_blueprint(booking_router)
    app.register_blueprint(user_router)
    app.register_blueprint(auth_router)
    app.register_blueprint(table_router)

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'message': 'Object not found.'}), 404

    return app


if __name__ == '__main__':
    app = create_app()

    app.run(port=app.config["PORT"])
