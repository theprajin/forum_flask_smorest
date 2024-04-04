from flask import Flask, jsonify
from flask_smorest import Api

from . import configurations
from .extensions import db, jwt, cors, migrate
from src.common.service import register_all_models
from src.common.exceptions import UnauthorizedAccess


def create_app():
    app = Flask(__name__)
    app.config.from_object(configurations.DevelopmentConfig)
    cors.init_app(app)
    db.init_app(app)

    from src.permissions.models import ContentType

    from src.common.models import AutoRegisterModel
    from src.posts.models import Post
    from src.comments.models import Comment
    from src.categories.models import Category
    from src.threads.models import Thread
    from src.tags.models import Tag
    from src.users.models import User
    from src.post_views.models import PostView

    with app.app_context():
        register_all_models()

    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.errorhandler(UnauthorizedAccess)
    def handle_unauthorized_access(error):
        return jsonify({"code": 401, "error": "Unauthorized Access"}), 401

    from src.posts import routes as posts_routes
    from src.comments import routes as comments_routes
    from src.categories import routes as categories_routes
    from src.threads import routes as threads_routes
    from src.tags import routes as tags_routes
    from src.auth import routes as auth_routes
    from src.users import routes as users_routes

    api = Api(app)
    api.register_blueprint(categories_routes.category_blp)
    api.register_blueprint(posts_routes.post_blp)
    api.register_blueprint(comments_routes.comment_blp)
    api.register_blueprint(threads_routes.thread_blp)
    api.register_blueprint(tags_routes.tag_blp)
    api.register_blueprint(auth_routes.auth_blp)
    api.register_blueprint(users_routes.user_blp)

    return app
