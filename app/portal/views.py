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
        if form.link.data is not None:
            old_po = Portal.query.filter_by(link=form.link.data).first()
            if old_po is not None:
                flash('portal link重复,添加失败!<a href="%s">点击查看重复的po</a>'
                      % url_for('portal.portal_info', po_id=old_po.id, _external=True))
                return redirect(url_for('portal.add'))
        po = Portal(name=form.name.data, area=form.area.data,
                    link=form.link.data, submitter_id=current_user.id)
        db.session.add(po)
        flash('添加成功, Thank you~<a href="%s">点击查看新添加的po</a>'
              % url_for('portal.portal_info', po_id=po.id, _external=True))
        return redirect(url_for('portal.add'))
    return render_template('portal/add.html', form=form)


@portal.route('/modify/<po_id>', methods=['GET', 'POST'])
# @permission_required(Permission.MODIFY_PORTAL)
def modify(po_id):
    po = Portal.query.get_or_404(po_id)
    if current_user.can(Permission.MODIFY_PORTAL) or po.submitter_id == current_user.id:
        form = AddPortalForm()
        if form.validate_on_submit():
            po.name = form.name.data
            po.link = form.link.data
            po.area = form.area.data
            db.session.add(po)
            return redirect(url_for('portal.portal_info', po_id=po_id))
        form.name.data = po.name
        form.link.data = po.link
        form.area.data = po.area
        return render_template('portal/modify.html', form=form, portals=[po])
    else:
        flash('抱歉, 只有po提交者和管理员才能修改po信息.')
        return redirect(url_for('portal.portal_info', po_id=po_id))


@portal.route('/change_amount/<po_id>')
def change_amount(po_id):
    pass


@portal.route('/submit_by/<username>')
def submit_by(username):
    pass
