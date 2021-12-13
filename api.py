# 吴彬宇
import json
import os
from UseSqlite import RiskQuery
from PIL import Image
from flask import Blueprint

api_bp = Blueprint("api_bp", __name__)


@api_bp.route("/api/json", methods=['GET', 'POST'])
def api():
    return json.dumps(get())  # 调用json.dumps方法将python对象转换成json对象


# 获取图片信息
def get():
    rq = RiskQuery('D:/2021.9Class/lan/PhotoString_by_ChenXintao/static/RiskDB.db')  # 数据库路径
    rq.instructions("SELECT * FROM photo ORDER By time desc")  # 读取数据表
    rq.do()
    data = []  # 定义空数组，用于存放图片信息
    for r in rq.format_results().split('\n\n'):
        lst = r.split(',')
        picture_time = lst[0].strip()  # 读取图片上传时间
        picture_desc = lst[1].strip()  # 读取图片描述
        picture_path = lst[2].strip()  # 读取图片储存路径
        picture_name = lst[3].strip()  # 读取图片命名
        picture_size = os.path.getsize(picture_path) // 1024  # 调用os.path.getsize方法获取图片大小
        js = {'picture_name': picture_name, 'picture_time': picture_time, 'picture_size': str(picture_size) +'KB', 'picture_desc': picture_desc}
        data.append(js)  # 将图片信息存入数组
    return data