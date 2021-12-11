# 吴彬宇
import json
import os
from UseSqlite import RiskQuery
from PIL import Image
from flask import Blueprint

api_bp = Blueprint("api_bp", __name__)


@api_bp.route("/api/json", methods=['GET', 'POST'])
# def make_json(s):
def api():
    return json.dumps(get())


def get():
    rq = RiskQuery('./static/RiskDB.db')
    rq.instructions("SELECT * FROM photo ORDER By time desc")
    rq.do()
    data = []
    for r in rq.format_results().split('\n\n'):
        lst = r.split(',')
        picture_time = lst[0].strip()
        picture_desc = lst[1].strip()
        picture_path = lst[2].strip()
        picture_name = lst[3].strip()
        picture_size = os.path.getsize(picture_path) // 1024
        js = {'picture_name': picture_name, 'picture_time': picture_time, 'picture_size': str(picture_size) +'KB', 'picture_desc': picture_desc}
        data.append(js)
    return data
