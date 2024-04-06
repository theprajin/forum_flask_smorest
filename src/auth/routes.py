from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from sqlalchemy.exc import IntegrityError
from src.extensions import db
from src.users.models import User
from src.users import crud as users_crud
from src.users.schemas import UserCreate, UserResponse, UserLogin
from src.users.exceptions import UserNotFound, UserAlreadyExists
from src.constants import URL_PREFIX
from .models import TokenBlockList

auth_blp = Blueprint(
    "Auth",
    __name__,
    url_prefix=f"{URL_PREFIX}/auth",
    description="Operations on Auth",
)


@auth_blp.route("/register")
class Register(MethodView):

    @auth_blp.arguments(UserCreate)
    @auth_blp.response(201, UserResponse)
    def post(self, new_data):
        """Register User"""
        try:

            email = new_data.get("email")
            users_crud.get_user_by_email(email)

            total_user = User.query.count()

            if total_user <= 0:
                users_crud.create_super_user(new_data)
            else:
                users_crud.create_user(new_data)
            return jsonify({"message": "user registration successful"}), 201

        except UserAlreadyExists:
            abort(409, message=f"User with email '{email}' already exists")
        except Exception as e:
            return str(e)


@auth_blp.route("/login")
class Login(MethodView):
    @auth_blp.arguments(UserLogin)
    @auth_blp.response(200, UserResponse)
    def post(self, new_data):
        """Login User"""
        try:
            email = new_data.get("email")
            password = new_data.get("password")

            user: User = users_crud.check_user_by_email(email)

            if not user or not user.verify_password(password):
                return jsonify({"error": "Incorrect email or password"}), 401

            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            return jsonify(access_token=access_token, refresh_token=refresh_token)
        except UserNotFound:
            abort(404, message=f"User with email '{email}' not found")
        except Exception as e:
            print(e)


@auth_blp.route("/refresh")
class AccessTokenWithRefreshToken(MethodView):

    @jwt_required(refresh=True)
    def post(self):
        """Create New Access Token With Refresh Token"""
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_access_token}, 200


@auth_blp.route("/logout")
class Logout(MethodView):

    @jwt_required()
    def post(self):
        """Logout User"""
        jti = get_jwt()["jti"]
        exists = TokenBlockList.query.filter_by(jti=jti).first()

        if not exists:
            try:
                db.session.add(TokenBlockList(jti=jti))
                db.session.commit()
                return jsonify({"message": "Logout Successful"}), 200
            except IntegrityError:
                db.session.rollback()
                return jsonify({"message": "Logout Failed"}), 500

        else:
            return jsonify({"message": "This token already expired"}), 500
