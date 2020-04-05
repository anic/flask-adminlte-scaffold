from app import get_logger, get_config
import math
import json
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask import jsonify
from app import utils
from app.models import User
from app.admin.forms import UserForm
from app.utils import load_mapping
from peewee import SQL
from werkzeug.utils import secure_filename
from . import admin
import os
from conf.config import config
from app.decorators import admin_required

logger = get_logger(__name__)
cfg = get_config()


@admin.route('/admin', methods=['GET'])
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"


@admin.route('/create_user', methods=['POST'])
@login_required
@admin_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        return form
    else:
        return 'fail'


@admin.route('/user', methods=['GET'])
@login_required
@admin_required
def query_user():
    limit = int(request.values.get('limit', cfg.ITEMS_PER_PAGE))
    limit = limit if limit > 0 else cfg.ITEMS_PER_PAGE

    offset = (int(request.values.get('offset', 0)) / limit)
    order = 'asc' if request.args.get('order', 'asc') == 'asc' else 'desc'
    query = User.select().where(User.status == 1)
    search = request.args.get('search')
    if search is not None and '' != search:
        query = query.where(User.username % ('*'+search+'*'))

    all = query.paginate(offset+1, limit)

    total = User.select().count()
    result = {
        'total': total,
        'totalNotFiltered': total,
        'rows': [p.to_dict() for p in all]
    }
    return result

# 通知方式配置
@admin.route('/user_list', methods=['GET'])
@login_required
@admin_required
def user_list():
    return render_template('admin/userlist.html', current_user=current_user)


@admin.route('/user_mapping', methods=['GET', 'POST'])
@login_required
@admin_required
def user_mapping():
    mapping = load_mapping('user_mapping')
    result = {
        'mapping': mapping
    }
    return result