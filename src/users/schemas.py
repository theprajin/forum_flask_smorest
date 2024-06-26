import marshmallow as ma
from marshmallow import validates, ValidationError
from email_validator import validate_email, EmailNotValidError

from src.roles.schemas import RoleBase


class UserCreate(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    first_name = ma.fields.String(required=True)
    last_name = ma.fields.String(required=True)
    email = ma.fields.Email(required=True)
    password = ma.fields.String(required=True)
    created_at = ma.fields.DateTime(dump_only=True)

    @validates("email")
    def validate_email(self, value):
        try:
            validate_email(value)
        except EmailNotValidError as e:
            raise ValidationError("Please provide a valid email address")
        return value

    @validates("password")
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError("Password must be at least 8 characters long")
        elif len(value) > 30:
            raise ValidationError("Password must be less than 30 characters long")
        return value


class UserResponse(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    first_name = ma.fields.String()
    last_name = ma.fields.String()
    is_admin = ma.fields.Boolean()
    email = ma.fields.Email()
    created_at = ma.fields.DateTime(dump_only=True)


class UserLogin(ma.Schema):
    email = ma.fields.Email(required=True)
    password = ma.fields.String(required=True)

    @validates("email")
    def validate_email(self, value):
        try:
            validate_email(value)
        except EmailNotValidError as e:
            raise ValidationError("Please provide a valid email address")
        return value

    @validates("password")
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError("Password must be at least 8 characters long")
        elif len(value) > 30:
            raise ValidationError("Password must be less than 30 characters long")
        return value


class UserRole(UserResponse):

    roles = ma.fields.List(ma.fields.Nested("RoleBase"), dump_only=True)


class RoleResponseSchema(RoleBase):
    users = ma.fields.Nested(
        UserRole, only=("id",), many=True, exclude=("role",), required=False
    )


class UserUpdate(ma.Schema):
    is_admin = ma.fields.Boolean(required=True)


class UserDetailResponse(UserResponse):
    roles = ma.fields.List(ma.fields.Nested("RoleBase"), dump_only=True)
    views = ma.fields.List(ma.fields.Nested("PostViewResponse", only=["id"]))
    posts = ma.fields.List(ma.fields.Nested("PostResponse", only=["id"]))
    comments = ma.fields.List(ma.fields.Nested("CommentResponse", only=["id"]))
    threads = ma.fields.List(ma.fields.Nested("ThreadResponse", only=["id"]))
