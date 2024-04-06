from flask import Flask, jsonify
from flask_smorest import Api
from sqlalchemy import inspect

from . import configurations
from .extensions import db, jwt, cors, migrate
from src.common.service import register_all_models
from src.common.exceptions import UnauthorizedAccess


def create_app():
    app = Flask(__name__)
    app.config.from_object(configurations.DevelopmentConfig)
    cors.init_app(app)
    db.init_app(app)

    # this creates the content_types table if it doesn't exist at the very beginning the app
    def create_content_types_table(app):
        with app.app_context():
            engine = db.engine
            inspector = inspect(engine)
            if not inspector.has_table("content_types"):
                from src.permissions.models import ContentType

                ContentType.__table__.create(engine)

    with app.app_context():
        create_content_types_table(app)

    # these are imported here so that db migration is done propery by flask-migrate
    from src.permissions.models import ContentType
    from src.common.models import AutoRegisterModel
    from src.posts.models import Post
    from src.comments.models import Comment
    from src.categories.models import Category
    from src.threads.models import Thread
    from src.tags.models import Tag
    from src.users.models import User
    from src.post_views.models import PostView
    from src.roles.models import Role
    from src.permissions.models import Permisssion
    from src.auth.models import TokenBlockList

    # this registers all the models that inherits from AutoRegisterModel
    with app.app_context():
        register_all_models()

    migrate.init_app(app, db)

    jwt.init_app(app)

    # this is to handle unathorized access
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
    from src.roles.routes import role_blp, role_perm_blp
    from src.permissions.routes import permission_blp, content_type_blp
    from src.post_views.routes import post_view_blp

    # this registers all the routes
    api = Api(app)
    api.register_blueprint(auth_routes.auth_blp)
    api.register_blueprint(users_routes.user_blp)
    api.register_blueprint(content_type_blp)
    api.register_blueprint(permission_blp)
    api.register_blueprint(role_blp)
    api.register_blueprint(role_perm_blp)
    api.register_blueprint(categories_routes.category_blp)
    api.register_blueprint(posts_routes.post_blp)
    api.register_blueprint(comments_routes.comment_blp)
    api.register_blueprint(threads_routes.thread_blp)
    api.register_blueprint(tags_routes.tag_blp)
    api.register_blueprint(post_view_blp)

    return app
