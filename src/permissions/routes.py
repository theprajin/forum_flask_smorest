from flask.views import MethodView
from flask_smorest import Blueprint, abort

from src.constants import URL_PREFIX
from src.permissions import crud
from src.permissions.exceptions import PermissionNotFound, ContentTypeNotFound
from src.permissions.schemas import PermissionBase, ContentTypeBase

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
    def post(self, permission_data):
        """Create Permission"""
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
    @permission_blp.doc(params={"id": "Permission ID"})
    def patch(self, permission_data, id):
        """Update Permission"""
        try:
            permission = crud.get_permission_or_404(id)

            return crud.update_permission(permission)
        except PermissionNotFound:
            abort(404, message=f"Permission with ID '{id}' not found")

    @permission_blp.doc(params={"id": "Permission ID"})
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
    def get(self):
        """Get Content Type List"""
        content_types = crud.get_content_type_list()
        return content_types


@content_type_blp.route("/<int:id>")
class ContentTypeByID(MethodView):
    @content_type_blp.response(200, ContentTypeBase)
    @content_type_blp.doc(params={"id": "Content Type ID"})
    def get(self, id):
        """Get Content Type"""
        try:
            content_type = crud.get_content_type_or_404(id)
            return content_type
        except ContentTypeNotFound:
            abort(404, message=f"Content Type with ID '{id}' not found")
