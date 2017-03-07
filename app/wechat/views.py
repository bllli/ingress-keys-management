# -*- coding: utf-8 -*-
import os
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.messages import *
from wechat_sdk.exceptions import ParseError
from flask import template_rendered, redirect, request, url_for


conf = WechatConf(
    token=os.environ.get('WECHAT_TOKEN') or 'your token',
    appid=os.environ.get('WECHAT_APPID') or 'your appid',
    appsecret=os.environ.get('WECHAT_APPSECRET') or 'your appsecret',
    encrypt_mode=os.environ.get('ENCRYPT_MODE') or 'your mode',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key=os.environ.get('ENCODING_AES_KEY') or 'your aes key'  # 如果传入此值则必须保证同时传入 token, appid
)

wechat = WechatBasic(conf=conf)

from . import keybot
from .doSomething import dosomething
from ..models import User
from flask_login import login_user
# from pymysql.err import OperationalError


@keybot.route('/interface', methods=['POST', 'GET'])
def interface():
    if request.method == 'GET':
        items = request.args.items()
        d = dict(items)
        try:
            signature = str(d['signature']).encode('utf-8')
            timestamp = str(d['timestamp']).encode('utf-8')
            nonce = str(d['nonce']).encode('utf-8')
            echostr = str(d['echostr']).encode('utf-8')
        except KeyError:
            return 'err', 500
        if wechat.check_signature(signature, timestamp, nonce):
            return echostr
        else:
            return 'Too simple!', 500

    if request.method == 'POST':
        items = request.args.items()
        d = dict(items)
        try:
            signature = str(d['signature']).encode('utf-8')
            timestamp = str(d['timestamp']).encode('utf-8')
            nonce = str(d['nonce']).encode('utf-8')
        except KeyError:
            return 'err', 500
        if wechat.check_signature(signature, timestamp, nonce):
            try:
                wechat.parse_data(request.get_data())
            except ParseError:
                print('Invalid Body Text')
                return wechat.response_text(content=u'服务器提了一个错误')
            source = wechat.message.source
            if isinstance(wechat.message, TextMessage):
                content = wechat.message.content.strip()
                response = dosomething(source, content)
                return wechat.response_text(content=response)
            if isinstance(wechat.message, EventMessage):
                if wechat.message.type == 'subscribe':
                    return wechat.response_text(content='欢迎使用ENL KEYS提交系统\n'
                                                        '请先设置昵称:"设置昵称 你的Agent Codename"\n'
                                                        '(大小写不敏感)')
            return wechat.response_text(content='这位特工我跟你讲,你发的是啥我看不懂!\n')
        else:
            return 'Sometimes naive.', 5000
