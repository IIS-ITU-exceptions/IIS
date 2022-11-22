from sqlalchemy import desc
from flask import Blueprint, request, jsonify, make_response, current_app, render_template
from flask_login import login_required, login_user, logout_user, current_user

from smartcity.views import roles_required
from smartcity.models import User, Role, RolesUsers, ServiceTask, ServiceTaskUsers, Comment, Ticket, TicketStateEnum, db


technician_bp = Blueprint("technician", __name__)


@technician_bp.route("/assigned_tasks", methods=["GET"])
@login_required
@roles_required(["technician"])
def assigned_tasks():
    tasks_for_user_STU = ServiceTaskUsers.query.filter(ServiceTaskUsers.user_id == current_user.id).all()
    service_tasks = []
    parent_tickets = []
    for task_STU in tasks_for_user_STU:
        service_tasks.append(ServiceTask.query.filter(ServiceTask.id == task_STU.service_task_id).all()[0])
    for task in service_tasks:
        parent_tickets.append(Ticket.query.filter(Ticket.id == task.parent_ticket).all()[0])
    return render_template("technician/assigned_tasks.html", current_user=current_user, service_tasks=service_tasks,
                           tickets=parent_tickets)

# @technician_bp.route("/assigned_tasks", methods=["GET"])
# @login_required
# @roles_required(["technician"])
# def assigned_tasks():
#     tickets = Ticket.query.filter(Ticket.assignee_id == current_user.id, Ticket.state != 'New').all()
#     return render_template("technician/assigned_tasks.html", current_user=current_user, tickets=tickets)
