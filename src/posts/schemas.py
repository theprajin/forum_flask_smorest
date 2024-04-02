import marshmallow as ma


class PostSchema(ma.Schema):
    title = ma.fields.String()
    content = ma.fields.String()


class PostCreateSchema(PostSchema):
    id = ma.fields.Integer(dump_only=True)
    title = ma.fields.String(required=True)
    content = ma.fields.String(required=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class PostResponseSchema(PostSchema):
    id = ma.fields.Integer(dump_only=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)
