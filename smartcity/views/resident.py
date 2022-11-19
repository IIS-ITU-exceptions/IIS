from flask import Blueprint, request, jsonify, make_response, current_app, render_template
from flask_login import login_required, login_user, logout_user, current_user
from . import roles_required
from ..models import User, Role, RolesUsers, ServiceTask, ServiceTaskUsers, Comment, Ticket, TicketStateEnum, db
from sqlalchemy import desc

from .resident_forms import *

resident_bp = Blueprint("resident", __name__)


@resident_bp.route("/new_ticket", methods=["GET", "POST"])
@login_required
@roles_required(["resident"])
def new_ticket():
    create_new_ticket_form = NewTicket()
    return render_template("resident/new_ticket.html", current_user=current_user, form=create_new_ticket_form)


@resident_bp.route("/my_tickets", methods=["GET"])
@login_required
@roles_required(["resident"])
def my_tickets():
    tickets = Ticket.query.filter(Ticket.reporter_id == current_user.id).order_by(desc(Ticket.id)).all()
    return render_template("resident/my_tickets.html", current_user=current_user, tickets=tickets)
