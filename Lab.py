# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:42:51 2019

@author: Administrator
"""

from flask import Flask, redirect, url_for
from show import show_bp
from api import api_bp

app = Flask(__name__)

# 将蓝图注册到app
# 1.注册show蓝图
# 2.注册api蓝图
app.register_blueprint(show_bp, url_prefix="/show")
app.register_blueprint(api_bp)

# 自己本地的项目绝对路径
ch = 'E:/JupyterWork/PhotoString_by_ChenXintao'


# 在运行主界面后，会自动执行此方法
@app.route('/', methods=['POST', 'GET'])
def show():
    # url_for 获取 show_bp.show的url地址
    # redirect 重定向到目标地址
    return redirect(url_for('show_bp.show'))


if __name__ == '__main__':
    app.run()
    app.run(debug=True)
