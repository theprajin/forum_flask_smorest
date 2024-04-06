from flask_smorest import abort
from sqlalchemy import desc
from .models import Post


def get_posts(queries):
    try:
        page = queries.get("page", 1)
        per_page = queries.get("page_size", 10)
        sortField = queries.get("sortField", "")
        sortDirection = queries.get("sortDirection", "asc")

        query = Post.query

        if "title" in queries:
            query = query.filter(Post.title.ilike(f"%{queries['title']}%"))

        if sortField == "title":
            if sortDirection == "desc":
                query = query.order_by(desc(Post.title))
            else:
                query = query.order_by(Post.title)

        posts = query.paginate(per_page=per_page, page=page, error_out=False)

        if not posts.items and page != 1:
            abort(404, message="No posts found")

        return posts.items

    except Exception as e:
        return str(e)
