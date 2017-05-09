# -*- coding: utf-8 -*-

from .. import db
from ..models import User, Portal, Have
from flask import render_template
from flask_login import login_user, current_user
from jinja2.exceptions import TemplateNotFound


def dosomething(source, content):
    """
    微信命令行???
    :param source: 某微信用户在本公众号上的id string
    :param content: 用户传来的命令字符串 string
    :return: 返回信息 string
    """
    content = content.strip()
    # 登录前允许的操作
    # 设置/修改昵称
    if content[:len(u"设置昵称")] == u"设置昵称":
        username = content[len(u"设置昵称"):].strip()
        import re
        p = re.compile(u'^[a-zA-Z0-9\u4e00-\u9fa5]+$')
        if username == '':
            return render_template('wechat/username/username_no_name.txt')
        elif not p.match(username):
            return render_template('wechat/username/username_wrong.txt')
        # elif user  # 正则匹配 u'^[a-zA-Z0-9\u4e00-\u9fa5]+$'
        user = User.query.filter_by(wechat_id=source).first()
        if user is not None:
            # 修改昵称
            if User.query.filter_by(username=username).first() is not None:
                # 已被占用，不允许重新设置
                return render_template('wechat/username/username_used.txt')
            else:
                # 未被占用，可以修改
                user.username = username
                db.session.add(user)
                return '昵称修改成功！'
        else:
            # 设置昵称
            if User.query.filter_by(username=username).first() is not None:
                # 已被占用，不允许重新设置
                return render_template('wechat/username/username_used.txt')
            else:
                user = User(username=username, wechat_id=source)
                db.session.add(user)
                return render_template('wechat/username/username_ok.txt')
    # 拦截未设置昵称的和未通过验证的用户的请求
    user = User.query.filter_by(wechat_id=source).first()
    if user is None:  # 没昵称请去设置昵称
        return render_template('wechat/auth/username_please.txt')
    if not user.confirmed:  # 没认证请联系管理员进行认证
        return render_template('wechat/auth/unconfirmed.txt')
    else:  # 认证了给个登录
        login_user(user, False)
    # 登陆后允许的操作
    if content[:len(u"list")].lower() == u"list":
        prep = content.split(' ')
        try:
            page = int(prep[1])
        except IndexError:
            page = 1
        except ValueError:
            return render_template('wechat/help/list.txt')
        if page <= 0:
            page = 1
        perpage = current_user.perpage if current_user.perpage < 50 else 50
        pagination = Portal.query.order_by(Portal.id.asc()).\
            paginate(page, per_page=perpage or 20, error_out=False)
        portals = pagination.items
        if len(portals) == 0:
            page = pagination.pages
            pagination = Portal.query.order_by(Portal.id.asc()).\
                paginate(page, per_page=perpage or 20, error_out=False)
            portals = pagination.items
        return render_template('wechat/po.txt', pagination=pagination, portals=portals)
    # 添加keys
    elif content[:len(u"key")].lower() == u"key":
        prep = content.split(' ')
        try:
            po_id = prep[1]
            count = int(prep[2])
        except IndexError:
            return render_template('wechat/help/key.txt')
        except ValueError:
            return render_template('wechat/key/should_be_number.txt')
        if not count > 0:
            return render_template('wechat/key/should_larger_than_zero.txt')
        po = Portal.query.filter_by(id=po_id).first()
        if po is not None:
            ha = Have.query.filter_by(portal_id=po_id,
                                      user_id=current_user.id).first()
            if ha is not None:
                ha.count = count
            else:
                ha = Have(portal_id=po_id, user_id=current_user.id, count=count)
            db.session.add(ha)
            db.session.commit()
            return render_template('wechat/po.txt', portals=[po])
        else:
            return render_template('wechat/key/wrong_portal_id.txt')
    elif content[:len(u"po")].lower() == u"po":
        prep = content.split(' ')
        try:
            po_id = prep[1]
        except IndexError:
            return render_template('wechat/help/po.txt')
        po = Portal.query.filter_by(id=po_id).first()
        if po is None:
            return render_template('wechat/help/po.txt', wrong_po_id=True)
        return render_template("wechat/po.txt", portals=[po], need_link=True)
    elif content[:len(u"perpage")].lower() == u"perpage":
        prep = content.split(' ')
        try:
            perpage = int(prep[1])
        except IndexError:
            return render_template('wechat/help/perpage.txt')
        except ValueError:
            return '分页数应该是一个十进制数～'
        if 10 <= perpage <= 100:
            current_user.perpage = perpage
            db.session.add(current_user)
            return '分页数已经设置为%d' % perpage
        else:
            return '分页数应在10~100之间'

    elif content[:len(u"whoami")].lower() == u"whoami":
        return '我认得你, 你是%s' % current_user.username
    elif content[:len(u"申请后台权限")] == u"申请后台权限":
        if current_user.login_confirmed:
            return '已经获得登录权限了'
        if current_user.login_request:
            return '请求已提交给管理员, 稍安毋躁'
        import random
        random_passwd = ''.join([random.choice("abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789")
                                 for i in range(8)])
        # 去掉了可能会引起误会的Oo0iIl1L
        current_user.login_request = True
        current_user.password = random_passwd
        current_user.passwd_changed = False
        db.session.add(current_user)
        return '您的请求已提交, 请联(督)系(促)管理员审核. 您的初始随机密码是%s.(密码只显示一次)' % random_passwd
    # 进阶操作介绍
    elif content[:len(u"more")].lower() == u"more":
        return render_template('wechat/help/more.txt')
    # 帮助
    elif content[:len(u"help")].lower() == u"help":
        prep = content.split(' ')
        try:
            code = prep[1]
        except IndexError:
            return render_template('wechat/help/help.txt')
        try:
            return render_template('wechat/help/%s.txt' % code)
        except TemplateNotFound:
            return '没找到该命令'
    return render_template('wechat/help/base.txt')
