import marshmallow as ma


class PermissionBase(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    can_create = ma.fields.Boolean(required=True)
    can_read = ma.fields.Boolean(required=True)
    can_delete = ma.fields.Boolean(required=True)
    can_modify = ma.fields.Boolean(required=True)
    content_type_id = ma.fields.Integer(required=True)
    created_at = ma.fields.DateTime(dump_only=True)


class ContentTypeBase(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    table_name = ma.fields.String(dump_only=True)
