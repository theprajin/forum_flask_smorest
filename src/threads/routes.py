from flask import jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from .schemas import ThreadResponse, ThreadCreate, ThreadUpdate
from .crud import (
    get_thread_list,
    get_thread_or_404,
    create_thread,
    update_thread,
    delete_thread,
)
from src.constants import URL_PREFIX
from .exceptions import ThreadNotFound
from src.comments.crud import get_comment_or_404
from src.comments.exceptions import CommentNotFound
from src.constants import URL_PREFIX
from src.common.dependencies import load_user_from_request
from src.common.exceptions import UnauthorizedAccess


thread_blp = Blueprint(
    "Threads",
    __name__,
    url_prefix=f"{URL_PREFIX}/threads",
    description="Operations on Threads",
)


@thread_blp.route("/")
class Thread(MethodView):
    @thread_blp.response(200, ThreadResponse(many=True))
    def get(self):
        """Get Thread List"""
        return get_thread_list()

    @thread_blp.arguments(ThreadCreate)
    @thread_blp.response(201, ThreadResponse)
    @load_user_from_request
    def post(self, thread_data):
        """Create Thread"""
        try:
            user_id = g.get("current_user").id
            comment_id = thread_data.get("comment_id")
            get_comment_or_404(comment_id)
            thread = create_thread(thread_data, user_id)
            return thread
        except CommentNotFound:
            abort(404, message=f"Comment with ID '{comment_id}' not found")
        except Exception as e:
            return str(e)


@thread_blp.route("/<int:thread_id>")
class ThreadByID(MethodView):
    @thread_blp.response(200, ThreadResponse)
    def get(self, thread_id):
        """Get Thread"""
        try:
            return get_thread_or_404(thread_id)
        except ThreadNotFound:
            abort(404, message=f"Thread with ID '{thread_id}' not found")
        except Exception as e:
            return str(e)

    @thread_blp.response(204)
    @load_user_from_request
    def delete(self, thread_id):
        """Delete Thread"""
        try:
            thread = get_thread_or_404(thread_id)
            if thread.user_id != g.get("current_user").id:
                raise UnauthorizedAccess
            delete_thread(thread_id)
        except ThreadNotFound:
            abort(404, message=f"Thread with ID '{thread_id}' not found")
        except UnauthorizedAccess:
            abort(403, message="You are not authorized to delete this thread")
        except Exception as e:
            return str(e)

    @thread_blp.arguments(ThreadUpdate)
    @thread_blp.response(200, ThreadResponse)
    @load_user_from_request
    def patch(self, thread_data, thread_id):
        """Update Thread"""
        try:
            thread = get_thread_or_404(thread_id)
            if thread.user_id != g.get("current_user").id:
                raise UnauthorizedAccess
            thread.title = thread_data.get("title") or thread.title
            thread.content = thread_data.get("content") or thread.content
            return update_thread(thread)
        except ThreadNotFound:
            abort(404, message=f"Thread with ID '{thread_id}' not found")
        except UnauthorizedAccess:
            abort(403, message="You are not authorized to update this thread")
        except Exception as e:
            return str(e)
