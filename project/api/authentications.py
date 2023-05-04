from functools import wraps
from flask import jsonify, request

from project.models import User, Role, BlacklistToken


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {"status": False,
                           "message": "Provide a valid auth token."}

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify(response_object), 401

        try:
            auth_token = auth_header.split(" ")[1]

            if BlacklistToken.check_blacklist(auth_token):
                response_object["message"] = "Token blacklisted. Please log in again."
                return jsonify(response_object), 401

        except:
            return jsonify(response_object), 401

        user_id = request.args.get('user_id')

        if user_id:
            if is_superadmin(auth_header):

                user = User.query.filter_by(id=user_id).first()

                if user:
                    return f(user_id, *args, **kwargs)

        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object["message"] = resp
            return jsonify(response_object), 401

        user = User.query.filter_by(id=resp).first()

        if not user or not user.is_active:
            return jsonify(response_object), 401

        if user.is_suspended:
            response_object["message"] = "Account suspended. Please contact admin."
            return jsonify(response_object), 401

        return f(resp, *args, **kwargs)

    return decorated_function


def require_secure_transport(f):
    @wraps(f)
    def is_https(*args, **kwargs):
        if request.scheme != "https":
            return (
                jsonify(
                    {
                        "status": False,
                        "message": "Endpoint MUST utilize https."
                    }
                ),
                400,
            )

        return f(*args, **kwargs)

    return is_https


def is_superadmin(auth_header):
    try:
        auth_token = auth_header.split(" ")[1]
    except:
        return False

    resp = User.decode_auth_token(auth_token)
    if isinstance(resp, str):
        return False

    user = User.query.filter_by(id=resp).first()

    if not user or not user.is_active:
        return False

    if user.is_suspended:
        return False

    if user.role == Role.ADMIN:
        return True

    return False
