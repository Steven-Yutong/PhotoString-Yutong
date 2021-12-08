# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:42:51 2019

@author: Administrator
"""

from flask import Flask, request
from UseSqlite import InsertQuery, RiskQuery
from datetime import datetime
from PIL import Image

app = Flask(__name__)
# 自己本地的项目绝对路径
ch = 'E:/JupyterWork/PhotoString_by_ChenXintao'


def make_html_paragraph(s):
    if s.strip() == '':
        return ''
    lst = s.split(',')
    picture_path = lst[2].strip()
    picture_name = lst[3].strip()
    im = Image.open(picture_path)
    im.thumbnail((400, 300))
    im.save(ch + '/static/figure/' + picture_name, 'jpeg')
    result = '<p>'
    result += '<i>%s</i><br/>' % (lst[0])
    result += '<i>%s</i><br/>' % (lst[1])
    result += '<a href="%s"><img src="./static/figure/%s"alt="风景图"></a>' % (picture_path, picture_name)
    return result + '</p>'


def get_database_photos():
    rq = RiskQuery(ch + '/static/RiskDB.db')
    rq.instructions("SELECT * FROM photo ORDER By time desc")
    rq.do()
    record = '<p>My past photo</p>'
    for r in rq.format_results().split('\n\n'):
        record += '%s' % (make_html_paragraph(r))
    return record + '</table>\n'


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        time_str = datetime.now().strftime('%Y%m%d%H%M%S')
        new_filename = time_str + '.jpg'
        uploaded_file.save(ch + '/static/upload/' + new_filename)
        time_info = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        description = request.form['description']
        path = ch + '/static/upload/' + new_filename
        iq = InsertQuery(ch + '/static/RiskDB.db')
        iq.instructions("INSERT INTO photo Values('%s','%s','%s','%s')" % (time_info, description, path, new_filename))
        iq.do()
        return '<p>You have uploaded %s.<br/> <a href="/">Return</a>.' % (uploaded_file.filename)
    else:
        page = '''<form action="/"method="post"enctype="multipart/form-data">
        <input type="file"name="file"><input name="description"><input type="submit"value="Upload"></form>'''
        page += get_database_photos()
        return page


if __name__ == '__main__':
    app.run(debug=True)