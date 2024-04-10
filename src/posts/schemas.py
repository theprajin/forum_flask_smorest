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


class PostQuery(ma.Schema):
    title = ma.fields.String(required=False)
    page = ma.fields.Int(required=False)
    per_page = ma.fields.Int(required=False)
    sortField = ma.fields.String(required=False)
    sortDirection = ma.fields.String(required=False, default="asc")


class PostDetailResponse(PostResponse):
    category = ma.fields.Nested("CategoryResponse", only=["id", "name"])
    user = ma.fields.Nested("UserResponse", only=["id", "first_name", "last_name"])
    tags = ma.fields.List(ma.fields.Nested("TagResponse", only=["id", "name"]))
    views = ma.fields.List(ma.fields.Nested("PostViewResponse", only=["id"]))
    comments = ma.fields.List(ma.fields.Nested("CommentResponse", only=["id"]))
    pass
