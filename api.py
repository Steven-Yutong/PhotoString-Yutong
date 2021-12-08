# 吴彬宇
from flask import Blueprint

api_bp = Blueprint("api_bp", __name__)


@api_bp.route("/json",methods=['GET', 'POST'])
def api():
    return "返回字符串"
