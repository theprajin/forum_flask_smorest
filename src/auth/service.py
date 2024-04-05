# Callback function to check if a JWT exists in the redis blocklist
from extensions import jwt, db
from src.auth.models import TokenBlockList


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_blocklist = (
        db.session.query(TokenBlockList).filter_by(jti=jti).one_or_none()
    )
    return token_in_blocklist is not None
