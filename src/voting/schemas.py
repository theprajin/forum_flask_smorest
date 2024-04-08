import marshmallow as ma


class VoteCreate(ma.Schema):
    id = ma.fields.Integer(dump_only=True)
    object_id = ma.fields.Integer(required=True)
    user_id = ma.fields.Integer(required=True)
    vote_type = ma.fields.Integer(required=True)
    content_type_id = ma.fields.Integer(required=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)

    @ma.post_load
    def make_vote(self, data, **kwargs):
        return data
