# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash, request, jsonify
from flask_login import login_required, current_user
from . import portal
from .. import db, csrf
from .forms import AddPortalForm
from ..models import Role, User, Permission, Portal, Have
from ..decorators import permission_required, admin_required
from flask_wtf.csrf import validate_csrf, ValidationError


@portal.route('/<po_id>')
@login_required
@permission_required(Permission.VIEW_AGENTS)
def portal_info(po_id):
    po = Portal.query.get_or_404(po_id)
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.last_seen.desc()).paginate(page, per_page=50, error_out=False)
    agents = pagination.items
    return render_template('portal/portal.html',
                           portals=[po], agents=agents, pagination=pagination, page=page, no_agents_row=True)


@portal.route('/add', methods=['POST', 'GET'])
@login_required
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
        db.session.commit()
        flash('添加成功, Thank you~<a href="%s">点击查看新添加的po</a>'
              % url_for('portal.portal_info', po_id=po.id, _external=True))
        return redirect(url_for('portal.add'))
    return render_template('portal/add.html', form=form)


@portal.route('/modify/<po_id>', methods=['GET', 'POST'])
# @permission_required(Permission.MODIFY_PORTAL)
@login_required
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


@portal.route('/all')
@permission_required(Permission.VIEW_AGENTS)
def all_portal():
    portals = Portal.query.order_by(Portal.id.asc()).all()
    agents = User.query.order_by(User.last_seen.desc()).all()
    return render_template('portal/all.html', portals=portals, agents=agents)


@portal.route('/change_count', methods=['POST'])
@csrf.exempt
def change_count():
    # 如果用户未登录，返回相关信息给AJAX，手动处理重定向。
    # 如果交给@login_required自动重定向的话，
    # AJAX不能正确处理这个重定向
    if not current_user.is_authenticated:
        return jsonify({
            'status': 302,
            'location': url_for(
                'auth.login',
                next=request.referrer.replace(
                    url_for('.index', _external=True)[:-1], ''))
        })
    # 以post方式传的数据在存储在的request.form中，以get方式传输的在request.args中~~
    # 同理，csrf token认证也要手动解决重定向
    try:
        validate_csrf(request.headers.get('X-CSRFToken'))
    except ValidationError:
        return jsonify({
            'status': 400,
            'location': url_for(
                'auth.login',
                next=request.referrer.replace(
                    url_for('.index', _external=True)[:-1], ''))
        })
    po_id = int(request.form.get('po_id'))
    count = int(request.form.get('count'))
    ha = Have.query.filter_by(portal_id=po_id,
                              user_id=current_user.id).first()
    if ha is not None:
        ha.count = count
    else:
        ha = Have(portal_id=po_id, user_id=current_user.id, count=count)
    db.session.add(ha)
    return 'ok'


@portal.route('/submit_by/<username>')
@login_required
def submit_by(username):
    pass
