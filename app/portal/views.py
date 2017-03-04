# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash, request
from flask_login import login_required, current_user
from . import portal
from .. import db
from .forms import AddPortalForm
from ..models import Role, User, Permission, Portal
from ..decorators import permission_required, admin_required


@portal.route('/<po_id>')
def portal_info(po_id):
    po = Portal.query.get_or_404(po_id)
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.last_seen.desc()).paginate(page, per_page=50, error_out=False)
    agents = pagination.items
    return render_template('portal/portal.html', portals=[po], agents=agents, pagination=pagination, page=page)


@portal.route('/add', methods=['POST', 'GET'])
@permission_required(Permission.ADD_PORTAL)
def add():
    form = AddPortalForm()
    if form.validate_on_submit():
        old_po = Portal.query.filter_by(link=form.link.data).first()
        if old_po is not None:
            flash('该portal已经被添加!<a href="%s">点击查看</a>' % url_for('portal.portal_info', po_id=old_po.id, _external=True))
            return redirect(url_for('portal.add'))
        po = Portal(name=form.name.data, area=form.area.data,
                    link=form.link.data, submitter_id=current_user.id)
        db.session.add(po)
        flash('添加成功, Thank you~')
        return redirect(url_for('portal.add'))
    return render_template('portal/add.html', form=form)


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
