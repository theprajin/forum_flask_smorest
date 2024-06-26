from flask.views import MethodView
from flask_smorest import Blueprint, abort

from src.constants import URL_PREFIX
from src.permissions import crud
from src.permissions.exceptions import PermissionNotFound, ContentTypeNotFound
from src.permissions.schemas import PermissionBase, ContentTypeBase
from src.common.dependencies import load_user_from_request, superuser_required

from src.constants import URL_PREFIX

permission_blp = Blueprint(
    "Permissions",
    __name__,
    url_prefix=f"{URL_PREFIX}/permissions",
)


@permission_blp.route("/")
class Permissions(MethodView):
    @permission_blp.response(200, PermissionBase(many=True))
    def get(self):
        """Get Permission List"""
        permissions = crud.get_permission_list()
        return permissions

    @permission_blp.arguments(PermissionBase)
    @permission_blp.response(201, PermissionBase)
    @superuser_required
    @load_user_from_request
    def post(self, permission_data):
        """Create Permission"""
        if permission_data.get("content_type_id") == 0:
            abort(400, message="Content type ID cannot be 0")
        permission = crud.create_permission(permission_data)
        return permission


@permission_blp.route("/<int:id>")
class PermissionByID(MethodView):
    @permission_blp.response(200, PermissionBase)
    @permission_blp.doc(params={"id": "Permission ID"})
    def get(self, id):
        """Get Permission"""
        try:
            permission = crud.get_permission_or_404(id)
            return permission
        except PermissionNotFound:
            abort(404, message=f"Permission with ID '{id}' not found")

    @permission_blp.arguments(PermissionBase)
    @permission_blp.response(200, PermissionBase)
    @superuser_required
    @load_user_from_request
    def patch(self, permission_data, id):
        """Update Permission"""
        try:
            permission = crud.get_permission_or_404(id)

            return crud.update_permission(permission)
        except PermissionNotFound:
            abort(404, message=f"Permission with ID '{id}' not found")

    @permission_blp.response(204)
    @superuser_required
    @load_user_from_request
    def delete(self, id):
        """Delete Permission"""
        try:
            permission = crud.get_permission_or_404(id)
            return crud.delete_permission(permission)
        except PermissionNotFound:
            abort(404, message=f"Permission with ID '{id}' not found")


# =======================================================================================================================


content_type_blp = Blueprint(
    "ContentTypes",
    __name__,
    url_prefix=f"{URL_PREFIX}/content-types",
)


@content_type_blp.route("/")
class ContentTypes(MethodView):
    @content_type_blp.response(200, ContentTypeBase(many=True))
    @superuser_required
    @load_user_from_request
    def get(self):
        """Get Content Type List"""
        content_types = crud.get_content_type_list()
        return content_types


@content_type_blp.route("/<int:id>")
class ContentTypeByID(MethodView):
    @content_type_blp.response(200, ContentTypeBase)
    @superuser_required
    @load_user_from_request
    def get(self, id):
        """Get Content Type"""
        try:
            content_type = crud.get_content_type_or_404(id)
            return content_type
        except ContentTypeNotFound:
            abort(404, message=f"Content Type with ID '{id}' not found")
