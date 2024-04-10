from flask.views import MethodView
from flask_smorest import Blueprint, abort


from .schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from .crud import (
    get_category_list,
    create_category,
    get_category_or_404,
    update_category,
    delete_category,
    get_category_by_name,
)
from .exceptions import CategoryNotFound, CategoryAlreadyExists
from src.constants import URL_PREFIX

category_blp = Blueprint(
    "Categories",
    __name__,
    url_prefix=f"{URL_PREFIX}/categories",
)


@category_blp.route("/")
class Category(MethodView):
    __model__ = "categories"

    @category_blp.response(200, CategoryResponse(many=True))
    def get(self):
        """Get Category List"""
        return get_category_list()

    @category_blp.arguments(CategoryCreate)
    @category_blp.response(201, CategoryResponse)
    def post(self, category_data):
        """Create Category"""
        try:
            name = category_data.get("name")
            get_category_by_name(name)
            return create_category(category_data)
        except CategoryAlreadyExists:
            abort(409, message=f"Category with name '{name}' already exists")
        except Exception as e:
            return str(e)


@category_blp.route("/<int:category_id>")
class CategoryByID(MethodView):
    __model__ = "categories"

    @category_blp.response(200, CategoryResponse)
    def get(self, category_id):
        """Get Category"""
        try:
            return get_category_or_404(category_id)
        except CategoryNotFound:
            abort(404, message=f"Category with ID '{category_id}' not found")
        except Exception as e:
            return str(e)

    @category_blp.arguments(CategoryUpdate)
    @category_blp.response(200, CategoryResponse)
    def patch(self, category_data, category_id):
        """Update Category"""
        try:
            category = get_category_or_404(category_id)
            category.name = category_data.get("name") or category.name
            return update_category(category)
        except CategoryNotFound:
            abort(404, message=f"Category with ID '{category_id}' not found")
        except Exception as e:
            return str(e)

    @category_blp.response(204)
    def delete(self, category_id):
        """Delete Category"""
        try:
            get_category_or_404(category_id)
            delete_category(category_id)

        except CategoryNotFound:
            abort(404, message=f"Category with ID '{category_id}' not found")
        except Exception as e:
            return str(e)
