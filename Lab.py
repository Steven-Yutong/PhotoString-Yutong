# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:42:51 2019

@author: Administrator
"""

from flask import Flask, request,redirect,url_for
from UseSqlite import InsertQuery, RiskQuery
from datetime import datetime
from PIL import Image
from test_blueprint import test_blueprint
from show import show_bp
from api import api_bp
from upload import upload_bp

app = Flask(__name__)

# 将蓝图注册到app
app.register_blueprint(show_bp, url_prefix="/show")
app.register_blueprint(upload_bp, url_prefix="/upload")
app.register_blueprint(api_bp, url_prefix="/api")

# 自己本地的项目绝对路径
ch='E:/JupyterWork/PhotoString_by_ChenXintao'


def make_html_paragraph(s):
    if s.strip()=='':
        return ''
    lst=s.split(',')
    picture_path=lst[2].strip()
    picture_name=lst[3].strip()
    im = Image.open(picture_path)
    im.thumbnail((400, 300))
    im.save(ch+'/static/figure/'+picture_name, 'jpeg')
    result='<p>'
    result+='<i>%s</i><br/>'%(lst[0])
    result+='<i>%s</i><br/>'%(lst[1])
    result+='<a href="%s"><img src="./static/figure/%s"alt="风景图"></a>'%(picture_path,picture_name)
    return result+'</p>'


def get_database_photos():
    rq = RiskQuery(ch + '/static/RiskDB.db')
    rq.instructions("SELECT * FROM photo ORDER By time desc")
    rq.do()
    record = '<p>My past photo</p>'
    for r in rq.format_results().split('\n\n'):
        record+='%s'%(make_html_paragraph(r))
    return record+'</table>\n'


@app.route('/', methods=['POST', 'GET'])
def show():
    return redirect(url_for('show_bp.show'))


if __name__ == '__main__':
    app.run()
    app.run(debug=True)
