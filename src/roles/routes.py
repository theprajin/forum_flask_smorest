from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from src.extensions import db
from src.constants import URL_PREFIX
from src.roles import crud
from src.roles.exceptions import RoleAlreadyExists, RoleNotFound
from src.roles.schemas import RoleBase, RolePermissions, RoleDetailResponse
from src.permissions.models import Permisssion
from src.permissions.crud import get_permission_or_404
from src.permissions.exceptions import PermissionNotFound
from src.common.dependencies import load_user_from_request, superuser_required

role_blp = Blueprint(
    "Roles",
    __name__,
    url_prefix=f"{URL_PREFIX}/roles",
)


@role_blp.route("/")
class Role(MethodView):
    @role_blp.response(200, RoleBase(many=True))
    def get(self):
        """Get Role List"""
        return crud.get_role_list()

    @role_blp.arguments(RoleBase)
    @role_blp.response(201, RoleBase)
    @superuser_required
    @load_user_from_request
    def post(self, role_data):
        """Create Role"""
        role = crud.create_role(role_data)
        return role


@role_blp.route("/<int:id>")
class RoleByID(MethodView):
    @role_blp.response(200, RoleDetailResponse)
    def get(self, id):
        """Get Role"""
        try:
            role = crud.get_role_or_404(id)
            return role
        except RoleNotFound:
            abort(404, message=f"Role with ID '{id}' not found")
        except Exception as e:
            return str(e)

    @role_blp.arguments(RoleBase)
    @role_blp.response(200, RoleBase)
    @superuser_required
    @load_user_from_request
    def patch(self, role_data, id):
        """Update Role"""
        try:
            role = crud.get_role_or_404(id)
            role.name = role_data.get("name") or role.name

            return crud.update_role(role)
        except RoleNotFound:
            abort(404, message=f"Role with ID '{id}' not found")
        except Exception as e:
            return str(e)

    @role_blp.response(204)
    @superuser_required
    @load_user_from_request
    def delete(self, id):
        """Delete Role"""
        try:
            crud.get_role_or_404(id)
            return crud.delete_role(id)
        except RoleNotFound:
            abort(404, message=f"Role with ID '{id}' not found")
        except Exception as e:
            return str(e)


# ==========================================================================================================================
# Role-Permission Routes


role_perm_blp = Blueprint(
    "role_permissions",
    __name__,
    url_prefix=f"{URL_PREFIX}/",
)


@role_perm_blp.route("/roles/<int:role_id>/permissions/<int:permission_id>")
class RolePermission(MethodView):

    @role_perm_blp.response(201, RolePermissions)
    @superuser_required
    @load_user_from_request
    def post(self, role_id, permission_id):
        """Assign Permission to Role"""

        try:

            role = crud.get_role_or_404(role_id)
            permission = get_permission_or_404(permission_id)

            if role is not None and permission is not None:
                for role_perm in role.permissions:
                    if role_perm.id == permission.id:
                        return jsonify({"message": "Permission already assigned"}), 400

                role.permissions.append(permission)
                db.session.commit()

                return role

        except RoleNotFound:
            abort(404, message=f"Role with ID '{role_id}' not found")
        except PermissionNotFound:
            abort(404, message=f"Permission with ID '{permission_id}' not found")
        except Exception as e:
            print(e)
