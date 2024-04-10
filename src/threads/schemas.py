import marshmallow as ma


class ThreadBase(ma.Schema):
    content = ma.fields.String()


class ThreadCreate(ThreadBase):
    id = ma.fields.Integer(dump_only=True)
    content = ma.fields.String(required=True)
    comment_id = ma.fields.Integer(required=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class ThreadResponse(ThreadBase):
    id = ma.fields.Integer(dump_only=True)
    comment_id = ma.fields.Integer(dump_only=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class ThreadUpdate(ma.Schema):
    comment_id = ma.fields.Integer(dump_only=True)


class ThreadDetailResponse(ThreadResponse):
    user = ma.fields.Nested("UserResponse", only=["id", "first_name", "last_name"])
