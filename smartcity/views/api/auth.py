import datetime

from flask import Blueprint, request, jsonify, make_response, current_app
from flask_login import login_required, login_user, logout_user, current_user
from datetime import datetime

from .. import roles_required
from ...models import User, Role, db, ServiceTaskUsers, ServiceTask, Comment, Ticket, TicketStateEnum, RolesUsers


auth_api_bp = Blueprint("auth_api", __name__)
UPLOAD_PATH = 'smartcity/static/images'


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
    # TODO NELZE ODSTRANIT UZIVATEL KDYZ VYTVORIL TICKET
    """
    (pymysql.err.IntegrityError)
     (1451, 'Cannot delete or update a parent row: a foreign key constraint fails (`smartcity`.`ticket`, CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`reporter_id`) REFERENCES `user` (`id`))')
[SQL: DELETE FROM user WHERE user.id = %(id_1)s]
[parameters: {'id_1': 7}]
    """
    data = request.get_json()
    with current_app.app_context():
        # user_to_delete = User.query.filter_by(id=data.get("id")).first()

        try:
            # db.session.query(RolesUsers).filter(RolesUsers.user_id == int(data.get("user_id"))).delete()
            # db.session.query(User).filter(User.id == int(data.get("user_id"))).delete()
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
            db.session.query(User).filter(User.id == int(data.get("user_id"))).update(
                {"email":data.get("email"),
                 "name":data.get("name"),
                 "surname":data.get("surname")
                 })
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
@roles_required(["resident"])
@auth_api_bp.route("/new_ticket", methods=["POST"])
def create_new_ticket():
    data = request.get_json()
    with current_app.app_context():
        try:
            new_ticket = Ticket(
                reporter_id=int(data.get("reporter_id")),
                name=data.get("name"),
                description=data.get("description"),
                image_path=data.get('image'), #image_path=img_path
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
# co se těch obrázků týče, tak v auth.py je uložím do smartcity/static/images a pak ukládám cestu, že?
