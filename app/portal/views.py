from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . import portal
from .. import db
from ..models import Role, User, Permission
from ..decorators import permission_required, admin_required


@portal.route('/<po_id>')
def portal_info(po_id):
    pass


@portal.route('/add')
@permission_required(Permission.ADD_PORTAL)
def add():
    pass


@portal.route('/modify/<po_id>')
@permission_required(Permission.MODIFY_PORTAL)
def modify(po_id):
    pass


@portal.route('/change_amount/<po_id>')
def change_amount(po_id):
    pass


@portal.route('/submit_by/<username>')
def submit_by(username):
    pass
