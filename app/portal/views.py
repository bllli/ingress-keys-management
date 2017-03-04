from flask import render_template, redirect, url_for, abort, flash, request
from flask_login import login_required, current_user
from . import portal
from .. import db
from ..models import Role, User, Permission, Portal
from ..decorators import permission_required, admin_required


@portal.route('/<po_id>')
def portal_info(po_id):
    po = Portal.query.get_or_404(po_id)
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.last_seen.desc()).paginate(page, per_page=50, error_out=False)
    agents = pagination.items
    return render_template('portal/portal.html', portals=[po], agents=agents, pagination=pagination, page=page)


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
