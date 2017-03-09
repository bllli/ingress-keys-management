# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash, request, jsonify
from flask_login import login_required, current_user
from . import admin
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
    pass


@admin.route('/insert_portals')
@login_required
@admin_required
def insert_portals():
    pass


@admin.route('/agent_set')
@login_required
@admin_required
def agent_set():
    pass
