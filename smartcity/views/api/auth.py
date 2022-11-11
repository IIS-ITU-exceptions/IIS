from flask import Blueprint, request, jsonify, make_response, current_app
from flask_login import login_required, login_user, logout_user, current_user
from ...models import User, Role, db

auth_api_bp = Blueprint("auth_api", __name__)


@auth_api_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    with current_app.app_context():
        user = User.query.filter_by(email=data.get("email")).first()

        if user:
            response_object = {
                "status": "fail",
                "message": "User already exists. Please log in.",
            }
            return make_response(jsonify(response_object), 202)
        else:
            try:
                new_user = User(
                    email=data.get("email"),
                    password=data.get("password"),
                    name=data.get("name"),
                    surname=data.get("surname"),
                )
                if data.get("role") == 1:
                    role = Role.query.filter_by(name="resident").first()
                    if not role:
                        raise AttributeError
                elif data.get("role") == 2:
                    role = Role.query.filter_by(name="technician").first()
                    if not role:
                        raise AttributeError
                elif data.get("role") == 3:
                    role = Role.query.filter_by(name="manager").first()
                    if not role:
                        raise AttributeError
                elif data.get("role") == 4:
                    role = Role.query.filter_by(name="admin").first()
                    if not role:
                        raise AttributeError
                new_user.role.append(role)
                db.session.expunge_all()
                db.session.add(new_user)
                db.session.commit()
                db.session.expunge_all()
                response_object = {
                    "status": "success",
                    "message": "User successfully registered.",
                }
                return make_response(jsonify(response_object), 201)
            except Exception as e:
                print(e)
                response_object = {
                    "status": "fail",
                    "message": "An error has occurred. Please try again.",
                }
                return make_response(jsonify(response_object), 500)


@auth_api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not current_user.is_anonymous:
        response_object = {
            "status": "fail",
            "message": "User already logged in.",
        }
        return make_response(jsonify(response_object), 401)

    with current_app.app_context():
        user = User.query.filter_by(email=data.get("email")).first()
        if not user:
            response_object = {
                "status": "fail",
                "message": "Incorrect credentials",
            }
            return make_response(jsonify(response_object), 401)
        else:
            if not user.verify_password(password=data.get("password")):
                response_object = {
                    "status": "fail",
                    "message": "Incorrect credentials.",
                }
                return make_response(jsonify(response_object), 401)
            else:
                login_user(user, remember=data.get("remember"))
                response_object = {
                    "status": "success",
                    "message": "User successfully logged in.",
                }
                return make_response(jsonify(response_object), 200)


@login_required
@auth_api_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    response_object = {
        "status": "success",
        "message": "User successfully logged out.",
    }
    return make_response(jsonify(response_object), 200)
