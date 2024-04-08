from src.extensions import db
from src.permissions.models import ContentType
from src.voting.models import Vote, VoteType
from .exceptions import (
    ContentTypeInvalid,
    NotVoteable,
    ModelAndContentTypeMismatch,
    VoteAlreadyExists,
)
from sqlalchemy.sql.schema import Table


def get_model_by_tablename(table_name):
    for model in db.Model.metadata.tables.items():
        if model[0] == table_name:
            return db.Model.metadata.tables[table_name]
    raise ContentTypeInvalid


def add_vote(user_id, content_type_name, object_id, vote_direction):
    content_type: ContentType = ContentType.query.filter_by(
        table_name=content_type_name
    ).first()

    if not content_type:
        raise ContentTypeInvalid

    model: Table = get_model_by_tablename(content_type_name)

    if content_type.table_name != model.name:
        raise ModelAndContentTypeMismatch

    query = db.session.query(model)
    voteable_object = query.filter_by(id=object_id).first()

    if voteable_object.voteable is False:
        raise NotVoteable(f"{content_type_name} is not voteable")

    vote = Vote.query.filter_by(
        user_id=user_id,
        content_type_id=content_type.id,
        object_id=object_id,
    ).first()

    if vote:
        print(f"vote direction: {vote_direction}")
        if vote_direction == 0:
            db.session.delete(vote)
            db.session.commit()
        elif vote.vote_type.value != vote_direction:
            vote.vote_type = VoteType.UP if vote_direction == 1 else VoteType.DOWN
            db.session.commit()
        elif vote.vote_type.value == vote_direction:
            raise VoteAlreadyExists

    else:
        new_vote = Vote(
            user_id=user_id,
            content_type_id=content_type.id,
            object_id=object_id,
            vote_type=VoteType.UP if vote_direction == 1 else VoteType.DOWN,
        )
        db.session.add(new_vote)
        db.session.commit()
    return vote
