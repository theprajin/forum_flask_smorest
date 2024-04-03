from flask.views import MethodView
from flask_smorest import Blueprint, abort

from src.constants import URL_PREFIX
from src.posts.crud import get_post_or_404
from src.posts.exceptions import PostNotFound
from .schemas import TagResponse, PostTag, TagBase
from . import crud
from .models import Tag
from .exceptions import TagNotFound, TagAlreadyExists

tag_blp = Blueprint(
    "Tags",
    __name__,
    url_prefix=f"{URL_PREFIX}/",
    description="Operations on Tags",
)


@tag_blp.route("/posts/<int:post_id>/tags")
class PostTags(MethodView):

    @tag_blp.response(200, PostTag(many=True))
    def get(self, post_id):
        """Get Post Tags"""
        post = get_post_or_404(post_id)

        return post.tags

    @tag_blp.arguments(TagBase)
    @tag_blp.response(201, TagResponse)
    def post(self, new_data, post_id):
        """Create Post Tag"""
        try:
            post = get_post_or_404(post_id)

            name = new_data.get("name")
            for post_tag in post.tags:
                if post_tag.name == name:
                    abort(409, message=f"Tag with name '{name}' already exists")

            tag = crud.create_tag(new_data, post)
            return tag
        except PostNotFound:
            abort(404, message=f"Post with ID '{post_id}' not found")
        except TagAlreadyExists:
            abort(409, message=f"Tag with name '{name}' already exists")


@tag_blp.route("posts/<int:post_id>/tags/<int:tag_id>")
class PostTagByID(MethodView):

    @tag_blp.response(200, TagResponse)
    def get(self, post_id, tag_id):
        """Get Post Tag"""
        try:
            post = get_post_or_404(post_id)
            tag = crud.get_tag_or_404(tag_id)
            return tag
        except PostNotFound:
            abort(404, message=f"Post with ID '{post_id}' not found")
        except TagNotFound:
            abort(404, message=f"Tag with ID '{tag_id}' not found")

    @tag_blp.response(204)
    def delete(self, post_id, tag_id):
        """Delete Post Tag"""
        try:
            post = get_post_or_404(post_id)
            tag = crud.get_tag_or_404(tag_id)
            crud.delete_tag(tag, post)

            return None
        except PostNotFound:
            abort(404, message=f"Post with ID '{post_id}' not found")
        except TagNotFound:
            abort(404, message=f"Tag with ID '{tag_id}' not found")
