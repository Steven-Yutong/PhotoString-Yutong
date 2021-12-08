# -*- coding: utf-8 -*-
from flask import Blueprint, request
# Blueprint必须制定两个参数:admin表示蓝图的名称，__name__表示蓝图所在模块
from UseSqlite import RiskQuery

test_blueprint = Blueprint('test_bluprint', __name__)

ch = 'E:/JupyterWork/PhotoString_by_ChenXintao'


@test_blueprint.route('/test', methods=['GET'])
def test():
    return "test success"


@test_blueprint.route('/upload')
def upload_bp():
    return "上传文档"


@test_blueprint.route('/show', methods=['GET', 'POST'])
def show_bp():
    rq = RiskQuery(ch + '/static/RiskDB.db')
    rq.instructions("SELECT * FROM photo ORDER By time desc")
    rq.do()
    record = '<p>My past photo</p>'
    for r in rq.format_results().split('\n\n'):
        r = r + 1
    return record + '</table>\n'


@test_blueprint.route('/show/query-string')
def search_bp():
    return "搜索图片"


@test_blueprint.route('/api/json')
def api_bp():
    return "返回json字符串"
