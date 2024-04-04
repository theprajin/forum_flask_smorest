from flask.views import MethodView
from flask_smorest import Blueprint, abort

from src.constants import URL_PREFIX
from src.roles import crud
from src.roles.exceptions import RoleAlreadyExists, RoleNotFound
from src.roles.schemas import RoleBase, RolePermissions
from src.permissions.models import Permisssion

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
    def post(self, role_data):
        """Create Role"""
        role = crud.create_role(role_data)
        return role


@role_blp.route("/<int:id>")
class RoleByID(MethodView):
    @role_blp.response(200, RoleBase)
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
    def delete(self, id):
        """Delete Role"""
        try:
            crud.get_role_or_404(id)
            return crud.delete_role(id)
        except RoleNotFound:
            abort(404, message=f"Role with ID '{id}' not found")
        except Exception as e:
            return str(e)
