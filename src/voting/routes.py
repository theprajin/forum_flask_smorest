from flask import jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from src.constants import URL_PREFIX
from src.extensions import db
from src.common.dependencies import load_user_from_request
from src.permissions.models import ContentType
from .models import Vote
from .schemas import VoteCreate
from .service import add_vote
from .exceptions import (
    ContentTypeInvalid,
    NotVoteable,
    ModelAndContentTypeMismatch,
    VoteAlreadyExists,
)


vote_blp = Blueprint(
    "Votes",
    __name__,
    url_prefix=f"{URL_PREFIX}/votes",
)


@vote_blp.route("/")
class Votes(MethodView):

    @vote_blp.arguments(VoteCreate)
    @load_user_from_request
    def post(self, new_data):
        """Add Vote"""
        user_id = g.get("current_user").id
        content_type_name = new_data.get("content_type_name")
        object_id = new_data.get("object_id")
        vote_direction = new_data.get("vote_direction")

        try:

            add_vote(
                user_id=user_id,
                content_type_name=content_type_name,
                object_id=object_id,
                vote_direction=vote_direction,
            )

        except ContentTypeInvalid:
            abort(400, message=f"Content type '{content_type_name}' is invalid")
        except NotVoteable:
            abort(400, message=f"Content type '{content_type_name}' is not voteable")

        except ModelAndContentTypeMismatch:
            abort(400, message=f"Model and Content type mismatch")
        except VoteAlreadyExists:
            abort(409, message=f"Vote already exists")

        except Exception as e:
            return str(e)

        return jsonify({"message": "Vote created successfully"}), 201
