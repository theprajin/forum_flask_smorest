from flask_smorest import abort
from src.extensions import db
from .models import Thread
from .exceptions import ThreadNotFound


def get_thread_list():
    return Thread.query.all()


def get_thread_or_404(id):
    thread = Thread.query.get(id)
    print(thread)
    if thread is None:
        raise ThreadNotFound
    return thread


def create_thread(thread_data, user_id):
    thread = Thread(**thread_data)
    thread.user_id = user_id
    db.session.add(thread)
    db.session.commit()
    return thread


def update_thread(thread):
    db.session.commit()
    return thread


def delete_thread(id):
    Thread.query.filter(Thread.id == id).delete()
    db.session.commit()
