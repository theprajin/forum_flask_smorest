from flask.views import MethodView
from flask_smorest import Blueprint, abort

from .schemas import UserCreate, UserResponse
from .crud import get_user_by_id, get_user_list
from .exceptions import UserAlreadyExists, UserNotFound
from src.constants import URL_PREFIX


user_blp = Blueprint(
    "Users",
    __name__,
    url_prefix=f"{URL_PREFIX}/users",
)


@user_blp.route("/")
class Users(MethodView):

    @user_blp.response(200, UserResponse(many=True))
    def get(self):
        """Get User List"""
        return get_user_list()


@user_blp.route("/<int:user_id>")
class UserByID(MethodView):

    @user_blp.response(200, UserResponse)
    def get(self, user_id):
        """Get User"""
        try:
            user = get_user_by_id(user_id)
            return user
        except UserNotFound:
            abort(404, message=f"User with ID '{user_id}' not found")
        except Exception as e:
            return str(e)
