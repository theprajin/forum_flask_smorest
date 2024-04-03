import marshmallow as ma


class TagBase(ma.Schema):
    id = ma.fields.Integer(dump_only=True)
    name = ma.fields.String(required=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class PostTag(ma.Schema):
    id = ma.fields.Integer(dump_only=True)
    name = ma.fields.String(dump_only=True)
    tags = ma.fields.List(ma.fields.Nested("TagBase"))
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class TagResponse(TagBase):
    posts = ma.fields.Nested(
        PostTag, only=("id",), many=True, exclude=["tags"], required=False
    )
