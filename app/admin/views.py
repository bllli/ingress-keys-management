# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash, request, jsonify
from flask_login import login_required, current_user
from . import admin
from .forms import PortalCSVForm
from .. import db
from ..models import Role, User, Permission, Portal, Have
from ..decorators import permission_required, admin_required


@admin.route('/')
@login_required
@admin_required
def index():
    pass


@admin.route('/agent_management')
@login_required
@admin_required
def agent_manage():
    agents = User.query.filter_by(confirmed=False).all()
    return render_template('admin/agent_management.html', agents=agents)


@admin.route('/agent_management/confirm/wechat/<user_id>')
@login_required
@admin_required
def agent_confirm_wechat(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.confirmed = True
    db.session.add(user)
    flash('已允许 %s 在微信提交keys.' % user.username)
    return redirect(url_for('admin.agent_manage'))


@admin.route('/insert_portals', methods=['POST', 'GET'])
@login_required
@admin_required
def insert_portals():
    form = PortalCSVForm()
    if form.validate_on_submit():
        text = form.text.data
        # https://www.ingress.com/intel?ll=39.089453,117.178838&z=17&pll=39.089453,117.178838
        import re
        p = re.compile(u'https://(www\.|)ingress\.com/intel\?ll=(\d+\.\d+),(\d+\.\d+)&z=\d+&pll=(\d+\.\d+),(\d+\.\d+)')
        portals = []
        with open('temp.csv', 'wb+') as f:
            f.write(text.encode('utf-8'))
        with open('temp.csv', 'r') as f:
            import csv
            cf = csv.reader(f)
            for row in cf:
                try:
                    name = row[1]
                    area = row[2]
                    link = row[3]
                except IndexError:
                    print(row)
                    flash('格式有误!导入失败!')
                    return redirect(url_for('admin.insert_portals'))
                portals.append([name, area, link])
        for portal in portals:
            name = u'%s' % portal[0]
            area = u'%s' % portal[1]
            link = u'%s' % portal[2]
            m = p.match(link)
            if m is None:
                link = None
            old_po = Portal.query.filter_by(link=link).first()
            if old_po:
                if old_po.name == name:
                    continue
                else:
                    link = None
            po = Portal(name=name, area=area, link=link)
            db.session.add(po)
        flash('导入成功!')
        return redirect(url_for('main.index'))
    return render_template('admin/insert_portals.html', form=form)


@admin.route('/agent_set')
@login_required
@admin_required
def agent_set():
    pass
