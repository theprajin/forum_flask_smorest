import marshmallow as ma


class CategoryBase(ma.Schema):
    name = ma.fields.String()


class CategoryCreate(CategoryBase):
    id = ma.fields.Integer(dump_only=True)
    name = ma.fields.String(required=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class CategoryResponse(CategoryBase):
    id = ma.fields.Integer(dump_only=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class CategoryUpdate(CategoryBase):
    pass


class CategoryDetailResponse(CategoryResponse):
    posts = ma.fields.List(ma.fields.Nested("PostResponse", only=["id", "title"]))
