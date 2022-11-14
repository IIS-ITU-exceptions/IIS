from flask import Blueprint, request, jsonify, make_response, current_app, render_template
from flask_login import login_required, login_user, logout_user, current_user
from . import roles_required
from ..models import User, Role, RolesUsers, ServiceTask, ServiceTaskUsers, Comment, Ticket, TicketStateEnum, db

from .manager_forms import CreateTechnician, CreateServiceTask

manager_bp = Blueprint("manager", __name__)


@manager_bp.route("/manager_dashboard", methods=["GET"])
@login_required
@roles_required(["manager"])
def manager_dashboard():
    tickets = Ticket.query.all()
    all_users = User.query.all()
    return render_template("manager/manager_dashboard.html", current_user=current_user, tickets=tickets, all_users=all_users)


@manager_bp.route("/create_technician", methods=["GET", "POST"])
@login_required
@roles_required(["manager"])
def create_technician():
    create_technician_form = CreateTechnician()
    if request.method == "POST":
        if create_technician_form.validate():
            response_object = {
                "status": "success", "message": "Form verification successful"
            }
            return jsonify(response_object), 200
        else:
            return jsonify(create_technician_form.errors), 400
    return render_template("manager/create_technician.html", current_user=current_user, form=create_technician_form)


@manager_bp.route("/create_service_task", methods=["GET", "POST"])
@login_required
@roles_required(["manager"])
def create_service_task():
    tickets = Ticket.query.all()
    service_technicians = User.query.join(RolesUsers).filter(RolesUsers.role_id == 2).all()
    create_service_task_form = CreateServiceTask(service_technicians)
    return render_template("manager/create_service_task.html", current_user=current_user, form=create_service_task_form,
                           service_technicians=service_technicians, tickets=tickets)
