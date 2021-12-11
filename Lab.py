# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:42:51 2019

@author: Administrator
"""

from flask import Flask, request,redirect,url_for
from UseSqlite import InsertQuery, RiskQuery
from datetime import datetime
from PIL import Image
from show import show_bp
from api import api_bp
from upload import upload_bp

app = Flask(__name__)

# 将蓝图注册到app
app.register_blueprint(show_bp, url_prefix="/show")
# app.register_blueprint(upload_bp, url_prefix="/upload")
app.register_blueprint(api_bp)

# 自己本地的项目绝对路径
ch='E:/JupyterWork/PhotoString_by_ChenXintao'


@app.route('/', methods=['POST', 'GET'])
def show():
    return redirect(url_for('show_bp.show'))


if __name__ == '__main__':
    app.run()
    app.run(debug=True)
