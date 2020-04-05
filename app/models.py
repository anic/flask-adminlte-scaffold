# -*- coding: utf-8 -*-

from peewee import SqliteDatabase, MySQLDatabase, Model, CharField, BooleanField, IntegerField, ForeignKeyField
from playhouse.shortcuts import dict_to_model, model_to_dict
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login_manager
from conf.config import config
import json
import os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

# db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER,
#    passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)
db = SqliteDatabase(cfg.DB_FILE)


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)

    def to_dict(self):
        return model_to_dict(self)


# 管理员工号


class User(UserMixin, BaseModel):
    username = CharField()  # 用户名
    password = CharField()  # 密码
    fullname = CharField()  # 真实性名
    email = CharField()  # 邮箱
    phone = CharField()  # 电话
    status = BooleanField(default=True)  # 生效失效标识
    permission = IntegerField() # 权限

    def verify_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def can(self, permission):
        return self.permission is not None and (self.permission & permission) == permission
 
    def is_admin(self):
        return self.can(Permission.ADMIN)

    def to_dict(self):
        self.password = ''
        return model_to_dict(self)

class Permission:
    ADMIN = 0x01
    COMMON = 0x02

# 通知人配置
class CfgNotify(BaseModel):
    check_order = IntegerField()  # 排序
    notify_type = CharField()  # 通知类型：MAIL/SMS
    notify_name = CharField()  # 通知人姓名
    notify_number = CharField()  # 通知号码
    status = BooleanField(default=True)  # 生效失效标识


class Client(BaseModel):
    name = CharField()
    company = CharField()
    position = CharField()
    group = CharField()
    phone = CharField()
    wechat = CharField()
    dingding = CharField()
    qq = CharField()
    email = CharField()
    company_address = CharField()
    home_address = CharField()
    tag = CharField()
    preference = CharField()
    relation = CharField()
    cohesion = CharField()
    network = CharField()
    short_term = CharField()
    long_term = CharField()
    attr1 = CharField()
    attr2 = CharField()
    attr3 = CharField()
    creator = ForeignKeyField(User, related_name="creator")


@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == int(user_id))


# 建表
def create_table():
    db.connect()
    db.create_tables([CfgNotify, User, Client])
