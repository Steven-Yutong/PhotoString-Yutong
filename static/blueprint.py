from flask import Flask, Blueprint, render_template, request
from UseSqlite import RiskQuery
from Lab import make_html_paragraph

app = Flask(__name__)
app.register_blueprint()

testModule = Blueprint('testModule', __name__)


ch='E:/JupyterWork/PhotoString_by_ChenXintao'


@testModule.route('/upload')
def upload_bp():
    return "上传图片"


@testModule.route('/show', methods=['GET', 'POST'])
def show_bp():
    return "显示图片"


@testModule.route('/show/query-string')
def search_bp():
    return "搜索图片"


@testModule.route('/api/json')
def api_bp():
    return "返回json字符串"
