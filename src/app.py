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
    from src.comments.models import Comment

    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.route("/")
    def index():
        return {"message": "Hello World"}

    from src.posts import routes as posts_routes
    from src.comments import routes as comments_routes

    api = Api(app)
    api.register_blueprint(posts_routes.post_blp)
    api.register_blueprint(comments_routes.comment_blp)

    return app
