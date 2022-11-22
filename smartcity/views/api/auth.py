import datetime
import base64
import re

from datetime import datetime

from flask import Blueprint, request, jsonify, make_response, current_app, url_for
from flask_login import login_required, login_user, logout_user, current_user

from smartcity.views import roles_required
from smartcity.models import User, Role, db, ServiceTaskUsers, ServiceTask, Ticket, Comment

auth_api_bp = Blueprint("auth_api", __name__)


@auth_api_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    with current_app.app_context():
        user = User.query.filter_by(email=data.get("email")).first()
        if user:
            if user.email == data.get("email"):
                response_object = {
                    "status": "fail",
                    "message": "User already exists. Please log in.",
                }
                return make_response(jsonify(response_object), 401)
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
            if user.deactivated:
                response_object = {
                    "status": "fail",
                    "message": "User deactivated.",
                }
                return make_response(jsonify(response_object), 401)
            elif not user.verify_password(password=data.get("password")):
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
                role_name = user.role[0].name
                if role_name == "resident":
                    response_object.update({"location": url_for("resident.my_tickets")})
                elif role_name == "technician":
                    response_object.update({"location": url_for("technician.assigned_tickets")})
                elif role_name == "manager":
                    response_object.update({"location": url_for("manager.manager_dashboard")})
                elif role_name == "admin":
                    response_object.update({"location": url_for("admin.admin_dashboard")})

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


@login_required
@roles_required(["manager"])
@auth_api_bp.route("/create_service_task", methods=["POST"])
def create_service_task():
    data = request.get_json()
    with current_app.app_context():
        try:
            new_service_task = ServiceTask(
                name=data.get("name"),
                description=data.get("description"),
                creator_id=int(data.get("creator_id")),
                parent_ticket=int(data.get("parent_ticket")),
            )
            technician = User.query.filter_by(id=data.get("technician_id")).first()
            new_service_task.technicians.append(technician)
            db.session.expunge_all()
            db.session.add(new_service_task)

            db.session.flush()

            new_service_task_users = ServiceTaskUsers(
                user_id=data.get("technician_id"),
                service_task_id=new_service_task.id,
            )
            db.session.expunge_all()
            db.session.add(new_service_task_users)
            db.session.commit()
            db.session.expunge_all()

            db.session.flush()

            db.session.execute(
                "DELETE FROM service_task_users WHERE id NOT IN (SELECT * FROM (SELECT MIN(id) FROM service_task_users GROUP BY user_id, service_task_id) AS t)")
            db.session.commit()

            response_object = {
                "status": "success",
                "message": "Service task successfully created.",
            }
            return make_response(jsonify(response_object), 201)
        except Exception as e:
            print(e)
            response_object = {
                "status": "fail",
                "message": "An error has occurred. Please try again.",
            }
            return make_response(jsonify(response_object), 500)



@login_required
@roles_required(["admin"])
@auth_api_bp.route("/delete_user", methods=["POST"])
def delete_user():
    data = request.get_json()
    with current_app.app_context():
        try:
            db.session.query(User).filter(User.id == int(data.get("user_id"))).update({"deactivated": 1})
            db.session.commit()
            db.session.expunge_all()
        except Exception as e:
            print(e)
            response_object = {
                "status": "fail",
                "message": "An error has occurred. Please try again.",
            }
            return make_response(jsonify(response_object), 500)

    response_object = {
        "status": "success",
        "message": "User successfully deleted.",
    }
    return make_response(jsonify(response_object), 200)


@login_required
@roles_required(["admin"])
@auth_api_bp.route("/edit_user", methods=["POST"])
def edit_user():
    data = request.get_json()
    with current_app.app_context():
        try:
            if data.get("password") == "":
                db.session.query(User).filter(User.id == int(data.get("user_id"))).update(
                    {"email": data.get("email"),
                     "name": data.get("name"),
                     "surname": data.get("surname")
                     })
            else:
                user = User.query.filter_by(email=data.get("email")).first()
                db.session.query(User).filter(User.id == int(data.get("user_id"))).update(
                    {"email": data.get("email"),
                     "name": data.get("name"),
                     "surname": data.get("surname")
                     })
                user = User.query.filter_by(email=data.get("email")).first()
                user.password = data.get("password")

            db.session.commit()
            db.session.expunge_all()

            response_object = {
                "status": "success",
                "message": "User successfully deleted.",
            }
            return make_response(jsonify(response_object), 200)
        except Exception as e:
            print(e)
            response_object = {
                "status": "fail",
                "message": "An error has occurred. Please try again.",
            }
            return make_response(jsonify(response_object), 500)


@login_required
@roles_required(["manager"])
@auth_api_bp.route("/edit_state", methods=["POST"])
def edit_state():
    data = request.get_json()
    with current_app.app_context():
        try:
            db.session.query(Ticket).filter(Ticket.id == int(data.get("ticket_id"))).update(
                {"state": data.get("state")})
            db.session.commit()
            db.session.expunge_all()

            response_object = {
                "status": "success",
                "message": "State successfully changed.",
            }
            return make_response(jsonify(response_object), 200)
        except Exception as e:
            print(e)
            response_object = {
                "status": "fail",
                "message": "An error has occurred. Please try again.",
            }
            return make_response(jsonify(response_object), 500)


@login_required
@roles_required(["manager"])
@auth_api_bp.route("/add_comment", methods=["POST"])
def add_comment():
    data = request.get_json()
    with current_app.app_context():
        try:
            new_comment = Comment(
                content = data.get("content"),
                created_at = data.get("created_at"),
                ticket_id = data.get("ticket_id"),
                commenter_id = data.get("commenter_id")
            )
            db.session.add(new_comment)
            db.session.commit()
            db.session.expunge_all()

            response_object = {
                "status": "success",
                "message": "State successfully changed.",
            }
            return make_response(jsonify(response_object), 200)
        except Exception as e:
            print(e)
            response_object = {
                "status": "fail",
                "message": "An error has occurred. Please try again.",
            }
            return make_response(jsonify(response_object), 500)


@login_required
@roles_required(["resident"])
@auth_api_bp.route("/new_ticket", methods=["POST"])
def create_new_ticket():
    # data = request.data
    data = request.get_json()
    with current_app.app_context():
        try:
            new_ticket: Ticket
            rep = data.get("reporter_id")
            img = data.get('image')
            if img != '':
                img = img[len('data:image/'):]
                end = img[:img.find(';')]
                img = img[img.find(',')+1:]
                # img = re.sub('^data:image/', '', img)
                # # end = re.sub(';base64,.*', '', img)
                # img = re.sub('.+;base64,', '', img)
                dt = datetime.now().strftime("%m%d%Y%H%M%S")
                f = "/static/images/" + dt + rep + '.' + end
                with open('smartcity' + f, "wb") as fh:
                    fh.write(base64.b64decode(img))

                new_ticket = Ticket(
                    reporter_id=int(rep),
                    name=data.get("name"),
                    description=data.get("description"),
                    image_path=f,
                    created_at=datetime.now()
                )
            else:
                new_ticket = Ticket(
                    reporter_id=int(rep),
                    name=data.get("name"),
                    description=data.get("description"),
                    created_at=datetime.now()
                )

            db.session.expunge_all()
            db.session.add(new_ticket)
            db.session.commit()

            response_object = {
                "status": "success",
                "message": "Service task successfully created.",
            }
            return make_response(jsonify(response_object), 201)
        except Exception as e:
            print(e)
            response_object = {
                "status": "fail",
                "message": "An error has occurred. Please try again.",
            }
            return make_response(jsonify(response_object), 500)


# @login_required
# @roles_required(["resident"])
# @auth_api_bp.route("/my_tickets", methods=["POST"])
# def get_my_tickets():
#     return
