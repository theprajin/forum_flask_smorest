from flask import Flask
from flask_smorest import Api

from . import configurations
from .extensions import db, jwt, cors, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(configurations.DevelopmentConfig)
    cors.init_app(app)
    db.init_app(app)

    from src.posts.models import Post

    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.route("/")
    def index():
        return {"message": "Hello World"}

    from src.posts import routes as posts_routes

    api = Api(app)
    api.register_blueprint(posts_routes.post_blp)

    return app
