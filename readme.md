# flask-adminlte-handler
## 简介
flask-adminlte-handler是一个Python环境下的WEB后台管理系统脚手架，目标是用极少量的代码，快速构建小型WEB应用。请勿在大中型项目中进行尝试。  

1. 使用较传统的重后端+轻前端的方式，降低总体代码量
2. Web框架使用Flask，默认Jinja模版
3. ORM框架使用Peewee
4. 前端套用基于BootStrap的AdminLTE模板


## 第三方依赖
- peewee
- pymysql
- flask
- flask-script
- flask-wtf
- flask-login


## 环境配置
### venv虚拟环境安装配置
```
sudo pip3 install virtualenv
virtualenv venv
. venv/bin/activate
```

### 第三方依赖安装
```
pip3 install -r requirements.txt

```
### 系统参数配置
1. 编辑`config.py`， 修改SECRET_KEY及MySQL数据库相关参数
```
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret'
DB_HOST = '127.0.0.1'
DB_USER = 'foobar'
DB_PASSWD = 'foobar'
DB_DATABASE = 'foobar'
```

2. 编辑log-app.conf，修改日志路径
```
args=('/path/to/log/flask-rest-sample.log','a','utf8')
```

### 数据库初始化
1. 自动建表
直接运行`python3 models.py`

2. 插入管理员用户（默认admin/admin)
```
INSERT INTO `user` (`id`, `username`, `password`, `fullname`, `email`, `phone`, `status`,`permission`)
VALUES
	(1, 'admin', 'pbkdf2:sha1:1000$Km1vdx3W$9aa07d3b79ab88aae53e45d26d0d4d4e097a6cd3', '管理员', 'admin@admin.com', '18612341234', 1, 1);
```

### 启动应用
```
nohup ./manage.py runserver 2>&1 &
或
./run_app_dev.py (仅限测试)
```


## 项目目录结构
![](http://oh0ra6igz.bkt.clouddn.com/963uh.jpg)  
- /app/auth  用户认证相关代码
- /app/main  主要功能点相关代码
- /app/static  JS、CSS等静态文件
- /app/template  页面模版
- /app/models.py  Peewee模型
- /app/utils.py  工具模块
- /conf  系统参数及日志配置

## 定制功能
### 第一期
1. 录入客户信息
2. 列表和卡片展示客户信息

### 第二期
1. 不同的员工输入不可见，管理员能看到所有客户
2. 信息增删改功能作为零星增删修改，增加“批量操作”功能，即对单一要素，批量修改，这样就不需要每次都导excel；excel作为初次数据或重大数据更改时，批量导入。
3. 不需要所有表头都筛选。表头“个性标签”输入时不同标签数据可否用分号隔开，例如：苹果; 香蕉；雪梨，然后显示成一个一个小方块。
4. 增加3个自定义字段，后期我如何修改？
5. 打印需要给样例，稍后我做一个范例给你


## 相关学习文档
- [http://flask.pocoo.org](http://flask.pocoo.org)
- [https://flask-login.readthedocs.io](https://flask-login.readthedocs.io)
- [https://flask-script.readthedocs.io](https://flask-script.readthedocs.io)
- [https://flask-wtf.readthedocs.io](https://flask-wtf.readthedocs.io)
- [http://docs.peewee-orm.com](http://docs.peewee-orm.com)
- [https://almsaeedstudio.com/preview](https://almsaeedstudio.com/preview)
