Ingress-keys-management
======

基于Python Flask的多用户Portal key管理网站

使用了[Flasky](https://github.com/miguelgrinberg/flasky)

代码开源，不分蓝绿；欢迎issue， 欢迎pr。
## 功能简介
### 微信端
### 网页端

## 部署
### 准备

首先clone本项目

`git clone https://github.com/bllli/ingress-keys-management`

创建并进入virtualenv环境
``` bash
cd ingress-keys-management
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

在venv中安装所需包

`pip install -r requirements.txt`

国内建议使用豆瓣的pypi源

`pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com`

安装失败时可能是需要安装 python-dev

`sudo apt-get install python-dev`

### 配置环境变量

微信
```
WECHAT_TOKEN=token
WECHAT_APPID=appid
WECHAT_APPSECRET=appsecret
ENCRYPT_MODE=compatible
ENCODING_AES_KEY=aes key
```

邮箱
```
MAIL_USERNAME=你的QQ邮箱
MAIL_PASSWORD=QQ邮箱授权码
ENL_ADMIN=管理员邮箱
```
设置
```
ENL_CONFIG=production
```
### 创建数据库，钦定管理员
```
python manager.py db init
python manager.py db migrate
python manager.py deploy
```
请按提示输入管理员的用户名、邮箱和密码

### 试运行
`python manager.py runserver`

### 生产环境运行
使用 nginx+uwsgi

（此处略去nginx安装步骤）

uwsgi安装

`pip install uwsgi`

##### uwsgi配置
已将默认的uwsgi保存于config.ini，注意修改“指向网站目录”
```ini
[uwsgi]

# uwsgi 启动时所使用的地址与端口
socket = 127.0.0.1:8001

# 指向网站目录
chdir = /path/to/ingress-keys-management

# python 启动程序文件
wsgi-file = manage.py

# python 程序内用以启动的 application 变量名
callable = app

# 处理器数
processes = 1

# 线程数
threads = 1

#状态检测地址
stats = 127.0.0.1:9191
```

##### nginx配置
注意修改公网地址等配置
> /etc/nginx/sites-enabled/default

```
server {
      listen  80;
      server_name 999.999.999.999; #公网地址

      location / {
        include      uwsgi_params;
        uwsgi_pass   127.0.0.1:8001;  # 指向uwsgi 所应用的内部地址,所有请求将转发给uwsgi 处理
        uwsgi_param UWSGI_PYHOME /home/www/my_flask/venv; # 指向虚拟环境目录
        uwsgi_param UWSGI_CHDIR  /home/www/my_flask; # 指向网站根目录
        uwsgi_param UWSGI_SCRIPT manage:app; # 指定启动程序
      }
    }
```

运行
```
(venv虚拟环境下)uwsgi config.ini
```