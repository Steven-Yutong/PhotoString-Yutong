# 谢铭轩
from flask import Blueprint

upload_bp = Blueprint("upload_bp", __name__)


@upload_bp.route("/", methods=['GET', 'POST'])
def upload():
    return "上传图片"
