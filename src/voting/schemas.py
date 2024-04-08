import marshmallow as ma
from marshmallow import validates, ValidationError

from src.permissions.models import ContentType


class VoteCreate(ma.Schema):
    id = ma.fields.Integer(dump_only=True)
    object_id = ma.fields.Integer(required=True)
    vote_direction = ma.fields.Integer(required=True)
    content_type_name = ma.fields.Str(required=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)

    @validates("vote_direction")
    def validate_vote_direction(self, value):
        try:
            if value in [0, 1, -1]:
                return value
            else:
                raise ValidationError("Invalid vote direction. Must be 0 or 1 or -1")
        except Exception as e:
            raise ValidationError("Invalid vote direction. Must be 0 or 1 or -1")
