from sqlalchemy import desc
from flask import Blueprint, request, jsonify, make_response, current_app, render_template
from flask_login import login_required, login_user, logout_user, current_user

from smartcity.views import roles_required
from smartcity.models import User, Role, RolesUsers, ServiceTask, ServiceTaskUsers, Comment, Ticket, TicketStateEnum, db
from .admin_forms import EditUser

technician_bp = Blueprint("technician", __name__)


@technician_bp.route("/assigned_tasks", methods=["GET"])
@login_required
@roles_required(["technician"])
def assigned_tasks():
    service_tasks = ServiceTask.query.join(ServiceTaskUsers).filter(ServiceTaskUsers.user_id == current_user.id).all()
    users = User.query.filter_by(email=current_user.email).first()
    edit_form = EditUser(name=users.name, surname=users.surname, email=users.email, role=users.role[0].name)
    return render_template("technician/assigned_tasks.html", current_user=current_user, service_tasks=service_tasks, userProfileForm=edit_form)

@technician_bp.route("/task_view", methods=["GET", "POST"])
@login_required
@roles_required(["technician", "manager"])
def task_view():
    if request.method == "GET":
        ticket = Ticket.query.join(ServiceTask).filter(Ticket.id == request.args.get("parent")).all()
        comments = Comment.query.filter(Comment.ticket_id == ticket[0].id).all()
        task = ServiceTask.query.filter(ServiceTask.id == request.args.get("taskID")).all()
    users = User.query.filter_by(email=current_user.email).first()
    edit_form = EditUser(name=users.name, surname=users.surname, email=users.email, role=users.role[0].name)
    return render_template("technician/task_view.html", current_user=current_user, ticket=ticket,
                           comments=comments, task=task, userProfileForm=edit_form)
