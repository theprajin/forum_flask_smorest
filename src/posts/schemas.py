import marshmallow as ma


class PostBase(ma.Schema):
    title = ma.fields.String()
    content = ma.fields.String()


class PostCreate(PostBase):
    id = ma.fields.Integer(dump_only=True)
    title = ma.fields.String(required=True)
    content = ma.fields.String(required=True)
    category_id = ma.fields.Integer(required=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    id = ma.fields.Integer(dump_only=True)
    category_id = ma.fields.Integer(dump_only=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)
