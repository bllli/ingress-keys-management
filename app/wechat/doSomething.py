# -*- coding: utf-8 -*-

from .. import db
from ..models import User
from flask_login import login_user


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
        pass
    elif content[:len(u"key")] == u"key":
        pass
    elif content[:len(u"po")] == u"po":
        pass
    return '蛤?\n' \
           '命令如下:\n' \
           '查看portal列表: "list"\n' \
           '查看po信息: "po <po编号>"\n' \
           '更改指定po的key数: "key <po编号> <key数量>"'
