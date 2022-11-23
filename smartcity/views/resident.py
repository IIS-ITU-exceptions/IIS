"""
File containing functions that renders resident's views

@author: David Novák
@email: xnovak2r@stud.fit.vutbr.cz
"""

from sqlalchemy import desc
from flask import Blueprint, request, jsonify, make_response, current_app, render_template
from flask_login import login_required, login_user, logout_user, current_user

from smartcity.views import roles_required
from smartcity.models import User, Role, RolesUsers, ServiceTask, ServiceTaskUsers, Comment, Ticket, TicketStateEnum, db
from smartcity.views.resident_forms import *
from .admin_forms import EditUser
resident_bp = Blueprint("resident", __name__)


@resident_bp.route("/new_ticket", methods=["GET", "POST"])
@login_required
@roles_required(["resident"])
def new_ticket():
    create_new_ticket_form = NewTicket()
    users = User.query.filter_by(email=current_user.email).first()
    edit_form = EditUser(name=users.name, surname=users.surname, email=users.email, role=users.role[0].name)
    return render_template("resident/new_ticket.html", current_user=current_user, form=create_new_ticket_form, userProfileForm=edit_form)


@resident_bp.route("/my_tickets", methods=["GET", "POST"])
@login_required
@roles_required(["resident"])
def my_tickets():
    users = User.query.filter_by(email=current_user.email).first()
    edit_form = EditUser(name=users.name, surname=users.surname, email=users.email, role=users.role[0].name)
    tickets = Ticket.query.filter(Ticket.reporter_id == current_user.id).order_by(desc(Ticket.id)).all()
    return render_template("resident/my_tickets.html", current_user=current_user, tickets=tickets, userProfileForm=edit_form)


@resident_bp.route("/map_of_tickets", methods=["GET", "POST"])
@login_required
@roles_required(["resident"])
def map_of_tickets():
    users = User.query.filter_by(email=current_user.email).first()
    edit_form = EditUser(name=users.name, surname=users.surname, email=users.email, role=users.role[0].name)
    return render_template("resident/map_of_tickets.html", current_user=current_user, userProfileForm=edit_form)
