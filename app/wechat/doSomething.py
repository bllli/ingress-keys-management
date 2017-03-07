# -*- coding: utf-8 -*-

from .. import db
from ..models import User, Portal
from flask import render_template
from flask_login import login_user, current_user


def dosomething(source, content):
    # 大小写不敏感
    content = content.strip().lower()

    # 设置/修改昵称
    if content[:len(u"设置昵称")] == u"设置昵称":
        username = content[len(u"设置昵称"):].strip()
        if username == '':
            return '请使用 “设置昵称" + 空格 + 你想起的昵称 来设置昵称'
        # elif user  # Todo: 正则匹配 u'[a-zA-Z0-9\u4e00-\u9fa5]+'
        user = User.query.filter_by(wechat_id=source).first()
        if user is not None:
            # 修改昵称
            if User.query.filter_by(username=username).first() is not None:
                # 已被占用，不允许重新设置
                return '此昵称已被占用=。=|||'
            else:
                # 未被占用，可以修改
                user.username = username
                db.session.add(user)
                return '昵称修改成功！'
        else:
            # 设置昵称
            if User.query.filter_by(username=username).first() is not None:
                # 已被占用，不允许重新设置
                return '此昵称已被占用=。=|||'
            else:
                user = User(username=username, wechat_id=source)
                db.session.add(user)
                return 'Agent code设置完成。\n' \
                       '请联系管理员获取操作权限\n' \
                       '命令如下:\n' \
                       '查看portal列表: "list"\n' \
                       '查看po信息: "po <po编号>"\n' \
                       '更改指定po的key数: "key <po编号> <key数量>"'

    # 拦截未设置昵称的和未通过验证的用户的请求
    user = User.query.filter_by(wechat_id=source).first()
    if user is None:  # 没昵称请去设置昵称
        return '请先使用 “设置昵称” + 空格 + 你想起的昵称 来设置昵称'
    if not user.confirmed:  # 没认证请联系管理员进行认证
        return '您没有该操作权限, 请联系管理员.'
    else:  # 认证了给个登录
        login_user(user, False)
    if content[:len(u"list")] == u"list":
        prep = content.split(' ')
        try:
            page = int(prep[1])
        except IndexError:
            page = 1
        except ValueError:
            return '查看po列表: "list <页数>"\n' \
                   '页数请输入数字'
        pagination = Portal.query.order_by(Portal.id.asc()).paginate(page, per_page=30, error_out=False)
        portals = pagination.items
        return render_template('wechat/po.txt', pagination=pagination, portals=portals)
    elif content[:len(u"key")] == u"key":
        pass
    elif content[:len(u"po")] == u"po":
        prep = content.split(' ')
        try:
            po_id = prep[1]
        except IndexError:
            return '查看po信息: "po <po编号>"\n' \
                   '没找到po编号'
        po = Portal.query.filter_by(id=po_id).first()
        if po is None:
            return '没找到编号对应的po\n' \
                   '请试试"list"查看po列表'
        return render_template("wechat/po.txt", portals=[po])

    return '蛤?\n' \
           '命令如下:\n' \
           '查看portal列表: "list"\n' \
           '查看po信息: "po <po编号>"\n' \
           '更改指定po的key数: "key <po编号> <key数量>"'
