import marshmallow as ma


class RoleBase(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String(required=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class RolePermissions(RoleBase):
    permissions = ma.fields.List(ma.fields.Nested("PermissionBase"), dump_only=True)


class RoleDetailResponse(RoleBase):
    permissions = ma.fields.List(ma.fields.Nested("PermissionBase"), dump_only=True)
    users = ma.fields.List(
        ma.fields.Nested("UserResponse", only=["id", "first_name", "last_name"])
    )
