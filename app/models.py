# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager


class Permission:
    WECHAT_LOGIN  = 0x001  # 微信端登陆
    WEB_LOGIN     = 0x002  # 网页端登陆
    ADD_PORTAL    = 0x004  # 增加新po
    MODIFY_PORTAL = 0x008  # 修改po信息, 比如补充po intel link
    VIEW_ALL_POS  = 0x010  # 查看所有portal
    VIEW_AGENTS   = 0x020  # 查看所有特工
    VERIFY_AGENTS = 0x040  # 认证特工
    MANAGE_GROUPS = 0x080  # 管理分组
    MANAGE_AGENTS = 0x100  # 管理特工（可修改特工权限，但不能修改其他管理员或超级管理员的权限，也不能设置管理员）
    ADMINISTER    = 0x800

    base_permissions = WECHAT_LOGIN | WEB_LOGIN | ADD_PORTAL
    # 基本权限， 包括登陆网页端和微信端 可以添加po
    trusty_agent = base_permissions | MODIFY_PORTAL | VIEW_ALL_POS
    # 可信的特工：在基本权限的基础上，允许修改po信息，并且可以查看所有po
    intel_user = trusty_agent | VIEW_AGENTS
    # intel使用者，可以看到所有特工的key情况
    intel_manager = intel_user | MANAGE_GROUPS
    # intel管理者，可以管理po分组和agent分组（此功能暂未实现）
    manager = intel_manager | MANAGE_AGENTS | VERIFY_AGENTS
    # 权限很大的管理员 可以认证、管理用户（管理用户功能暂未实现）
    administrator = 0xfff
    # 超级管理员， 想干啥干啥


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'WechatUser': (Permission.WECHAT_LOGIN | Permission.ADD_PORTAL, True),
            'User': (Permission.base_permissions, False),
            'TrustyAgent': (Permission.trusty_agent, False),
            'IntelUser': (Permission.intel_user, False),
            'IntelManager': (Permission.intel_manager, False),
            'Manager': (Permission.manager, False),
            'Administrator': (0xfff, False),
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class Portal(db.Model):
    __tablename__ = 'portals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    area = db.Column(db.String(128))
    link = db.Column(db.String(128), unique=True)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    submitter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    keys = db.relationship('Have', backref='portal', lazy='dynamic')

    def __repr__(self):
        return '<Portal %r>' % self.name


class Have(db.Model):
    __tablename__ = 'haves'
    portal_id = db.Column(db.Integer, db.ForeignKey('portals.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    count = db.Column(db.Integer, default=0)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Have %d @ %r by user%d>' % (self.count, self.portal_id, self.user_id)

    @staticmethod
    def ping(target, value, oldvalue, initiator):
        target.timestamp = datetime.utcnow()
db.event.listen(Have.count, 'set', Have.ping)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    login_request = db.Column(db.Boolean)
    login_confirmed = db.Column(db.Boolean, default=False)
    passwd_changed = db.Column(db.Boolean, default=False)

    wechat_id = db.Column(db.String(128))
    perpage = db.Column(db.Integer, default=20)

    banned = db.Column(db.Boolean, default=False)
    banner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bans = db.relationship('User', backref='banner', remote_side='User.id')

    submit_portals = db.relationship('Portal', backref='submitter', lazy='dynamic')
    keys_having = db.relationship('Have', backref='haver', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ENL_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()
        if self.perpage is None:
            self.perpage = 20

    def having_key(self, po_id):
        # return Portal.query.join(Have, Have.portal_id == Portal.id).\
        #    filter(Have.user_id == self.id).first()
        # Have.query.join(Portal, Portal.id == Have.portal_id).filter(Have.user_id == self.id)
        have = Have.query.filter_by(portal_id=po_id, user_id=self.id).first()
        if have is not None:
            return have.count
        else:
            return 'n/a'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.username.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
