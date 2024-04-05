from flask import jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from src.common.dependencies import load_user_from_request, superuser_required
from src.extensions import db
from src.roles.exceptions import RoleNotFound
from .schemas import UserCreate, UserResponse, UserRole
from .crud import get_user_or_404, get_user_list
from .exceptions import UserAlreadyExists, UserNotFound
from src.roles.crud import get_role_or_404


from src.constants import URL_PREFIX


user_blp = Blueprint(
    "Users",
    __name__,
    url_prefix=f"{URL_PREFIX}/users",
)


@user_blp.route("/")
class Users(MethodView):

    @user_blp.response(200, UserResponse(many=True))
    @superuser_required
    @load_user_from_request
    def get(self):
        """Get User List"""
        return get_user_list()


@user_blp.route("/<int:user_id>")
class UserByID(MethodView):

    @user_blp.response(200, UserResponse)
    def get(self, user_id):
        """Get User"""
        try:
            user = get_user_or_404(user_id)
            return user
        except UserNotFound:
            abort(404, message=f"User with ID '{user_id}' not found")
        except Exception as e:
            return str(e)


@user_blp.route("/me")
class UserProfile(MethodView):

    @user_blp.response(200, UserResponse)
    @load_user_from_request
    def get(self):
        """Get Own User Profile"""

        try:
            user = g.current_user

            return user
        except Exception as e:
            print(e)


@user_blp.route("/<int:user_id>/roles/<int:role_id>")
class UserRoles(MethodView):

    @user_blp.response(201, UserRole)
    @superuser_required
    @load_user_from_request
    def post(self, user_id, role_id):
        """Assign Role to User"""

        try:

            user = get_user_or_404(user_id)
            role = get_role_or_404(role_id)

            if user is not None and role is not None:
                for user_role in user.roles:
                    if user_role.id == role.id:
                        return jsonify({"message": "Role already assigned"}), 400

                user.roles.append(role)
                db.session.commit()

                return user

            else:
                return jsonify({"message": f"User or Role does not exist"}), 404
        except UserNotFound:
            abort(404, message=f"User with ID '{user_id}' not found")
        except RoleNotFound:
            abort(404, message=f"Role with ID '{role_id}' not found")
        except Exception as e:
            print(e)

    @user_blp.response(204, UserRole)
    @superuser_required
    @load_user_from_request
    def delete(self, user_id, role_id):
        """Remove Role from User"""

        try:

            user = get_user_or_404(user_id)
            role = get_role_or_404(role_id)

            if user is not None and role is not None:
                for user_role in user.roles:
                    if user_role.id == role.id:
                        user.roles.remove(role)
                        db.session.commit()

                        return user

        except UserNotFound:
            abort(404, message=f"User with ID '{user_id}' not found")
        except RoleNotFound:
            abort(404, message=f"Role with ID '{role_id}' not found")
        except Exception as e:
            print(e)
