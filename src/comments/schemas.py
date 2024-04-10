import marshmallow as ma


class ComentBase(ma.Schema):
    content = ma.fields.String()


class CommentCreate(ComentBase):
    id = ma.fields.Integer(dump_only=True)
    content = ma.fields.String(required=True)
    post_id = ma.fields.Integer(required=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class CommentResponse(ComentBase):
    id = ma.fields.Integer(dump_only=True)
    post_id = ma.fields.Integer(dump_only=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class CommentUpdate(ComentBase):
    post_id = ma.fields.Integer(dump_only=True)


class CommentDetailResponse(CommentResponse):
    user = ma.fields.Nested("UserResponse", only=["id", "first_name", "last_name"])
    threads = ma.fields.List(ma.fields.Nested("ThreadResponse"))
    pass
