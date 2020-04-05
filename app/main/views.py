from app import get_logger, get_config
import math
import json
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask import jsonify
from app import utils
from app.models import CfgNotify, Client
from app.main.forms import CfgNotifyForm
from app.utils import load_mapping, import_excel
from peewee import SQL
from werkzeug.utils import secure_filename
from . import main
import os
from conf.config import config


logger = get_logger(__name__)
cfg = get_config()


# 通用列表查询
def common_list(DynamicModel, view):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get(
        'length') else cfg.ITEMS_PER_PAGE

    # 删除操作
    if action == 'del' and id:
        try:
            DynamicModel.get(DynamicModel.id == id).delete_instance()
            flash('删除成功')
        except:
            flash('删除失败')

    # 查询列表
    query = DynamicModel.select()
    total_count = query.count()

    # 处理分页
    if page:
        query = query.paginate(page, length)

    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template(view, form=dict, current_user=current_user)


# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        # 查询
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)
        # 修改
        if request.method == 'POST':
            if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.save()
                flash('修改成功')
            else:
                utils.flash_errors(form)
    else:
        # 新增
        if form.validate_on_submit():
            model = DynamicModel()
            utils.form_to_model(form, model)
            model.save()
            flash('保存成功')
        else:
            utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user)


# 根目录跳转
@main.route('/', methods=['GET'])
@login_required
def root():
    return redirect(url_for('main.index'))


# 首页
@main.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', current_user=current_user)


# 通知方式查询
@main.route('/notifylist', methods=['GET', 'POST'])
@login_required
def notifylist():
    return common_list(CfgNotify, 'notifylist.html')


# 通知方式配置
@main.route('/notifyedit', methods=['GET', 'POST'])
@login_required
def notifyedit():
    return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit.html')

# 通知方式配置
@main.route('/clientlist', methods=['GET'])
@login_required
def client_list():
    return render_template('main/clientlist.html', current_user=current_user)

# 通知方式配置
@main.route('/clientcard', methods=['GET'])
@login_required
def client_card():
    return render_template('main/clientcard.html', current_user=current_user)


@main.route('/client', methods=['GET', 'POST'])
@login_required
def client():
    # print(current_user.username)
    limit = int(request.values.get('limit', cfg.ITEMS_PER_PAGE))
    limit = limit if limit > 0 else cfg.ITEMS_PER_PAGE

    offset = (int(request.values.get('offset', 0)) / limit)
    order = 'asc' if request.args.get('order', 'asc') == 'asc' else 'desc'

    query = Client.select()
    search = request.args.get('search')
    if search is not None and '' != search:
        query = query.where(Client.name % ('*'+search+'*'))

    sort = request.args.get('sort')
    if sort is not None:
        sql_sort = SQL(sort).asc() if order == 'asc' else SQL(sort).desc()
        query = query.order_by(sql_sort)

    all = query.paginate(offset+1, limit)

    total = Client.select().count()
    result = {
        'total': total,
        'totalNotFiltered': total,
        'rows': [p.to_dict() for p in all]
    }
    return result


@main.route('/table_mapping', methods=['GET', 'POST'])
def table_mapping():
    mapping = load_mapping('table_mapping')
    result = {
        'mapping': mapping
    }
    return result


@main.route('/card_mapping', methods=['GET', 'POST'])
def card_mapping():
    mapping = load_mapping('card_mapping')
    result = {
        'mapping': mapping
    }
    return result


@main.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    filename = secure_filename(f.filename)
    filepath = os.path.join(cfg.UPLOAD_FOLDER, filename)
    f.save(filepath)

    result = {
        'files': [
            {
                'id':   '1',
                'name': secure_filename(f.filename),
                'type': 'xls',
                'size': 1,
                'url':  ''
            }
        ]
    }

    clients = import_excel(filepath)
    if len(clients) == 0:
        return result

    # 删除所有数据
    Client.delete().execute()
    # 插入所有数据
    Client.insert_many(clients).execute()

    return result
