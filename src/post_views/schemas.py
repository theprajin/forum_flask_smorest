import marshmallow as ma


class PostViewResponse(ma.Schema):
    id = ma.fields.Integer(dump_only=True)
    post_id = ma.fields.Integer(dump_only=True)
    user_id = ma.fields.Integer(dump_only=True)
    viewed_at = ma.fields.DateTime(dump_only=True)


class PostViewCreate(ma.Schema):
    id = ma.fields.Integer(dump_only=True)
    user_id = ma.fields.Integer(required=False)
    viewed_at = ma.fields.DateTime(dump_only=True)
