# ingress-keys-management
多用户Portal key管理网站

## 设想功能
- Web页
  - [ ] Portal信息
  - [ ] Portal标签/分类管理
  - [ ] Portal评论
  - [ ] Keys管理
- IITC插件
  - [ ] 用户手动上传Portal信息(只获取Po标题、图片url、位置等基本属性，如违反TOS请告知)
  - [ ] 按标签/分类查看Portal及用户Key
- Telegram Bot
  - [ ] 别瞅了 没想好呢

## For 开发者
### 技术选型
Django + Vue.js

### 开发环境部署

#### 准备
安装好
- Python3.6(个人推荐使用Anaconda3, 很方便)
- npm
#### 前端
```shell
cd frontend
npm install

# 安装并编译semantic-ui
sudo npm install gulp -g
cd semantic/
gulp build

# 切换回frontend目录
cd ..

# build 完成后注意看有没有出错 出错发issue
npm run build
```

#### 后端
```shell
# 安装所需包
pip install -r requirements.txt
# 国内建议使用豆瓣源加速下载
pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com

# 初始化数据库
python manage.py makemigrations
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 运行
python manage.py runserver

# 打开 http://127.0.0.1:8000
```

#### 正式部署时注意事项
- 将 `IngressKeyManagement/setting.py` 中的 `CORS_ORIGIN_ALLOW_ALL` 改为 `False`
- 修改IITC插件中的url
