# 吴雨桐 & 王炫

from flask import Blueprint, request
from UseSqlite import InsertQuery, RiskQuery
from PIL import Image
import datetime
show_bp = Blueprint("show_bp", __name__)

ch='E:/JupyterWork/PhotoString_by_ChenXintao'


@show_bp.route('/', methods=['GET', 'POST'])
def show():
    page = '''
<form action="/show/upload" method="post" enctype="multipart/form-data">
    <input type="file" name="file" />
    <input name="description" />
    <input type="submit"value="Upload" />
</form>
<form action="/show/search" method="post" enctype="multipart/form-data">
    <input type="text" name="search-str" />
    <input type="submit" value="检索" />
</form>
'''
    page += get_database_photos()
    return page


@show_bp.route('/search', methods=['GET', 'POST'])
def search():
    str = request.form['search-str']
    page = '''
    <form action="/show/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" />
        <input name="description" />
        <input type="submit"value="Upload" />
    </form>
    <form action="/show/search" method="post" enctype="multipart/form-data">
        <input type="text" name="search-str" />
        <input type="submit" value="检索" />
    </form>
    '''
    page += get_database_photos(str)
    return page


@show_bp.route("/upload", methods=['GET', 'POST'])
def upload():
    # if request.method == 'POST':
        uploaded_file = request.files['file']
        time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        new_filename = time_str + '.jpg'
        uploaded_file.save(ch + '/static/upload/' + new_filename)
        time_info = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        description = request.form['description']
        path = ch + '/static/upload/' + new_filename
        iq = InsertQuery(ch + '/static/RiskDB.db')
        iq.instructions("INSERT INTO photo Values('%s','%s','%s','%s')" % (time_info, description, path, new_filename))
        iq.do()
        return '<p>You have uploaded %s.<br/> <a href="/">Return</a>.' % (uploaded_file.filename)
    # else:
    #     page = '''<form action="/"method="post"enctype="multipart/form-data">
    #     <input type="file"name="file"><input name="description"><input type="submit"value="Upload"></form>'''
    #     page += get_database_photos()
    #     return page


def make_html_paragraph(s):
    if s.strip() == '':
        return ''
    lst = s.split(',')
    picture_path = lst[2].strip()
    picture_name = lst[3].strip()
    im = Image.open(picture_path)
    im.thumbnail((400, 300))
    im.save('./static/figure/' + picture_name, 'jpeg')
    result = '<p>'
    result += '<i>%s</i><br/>' % (lst[0])
    result += '<i>%s</i><br/>' % (lst[1])
    result += '<a href="%s"><img src="/static/figure/%s"alt="风景图"></a>' % (picture_path, picture_name)
    return result + '</p>'


def get_database_photos(str=''):
    rq = RiskQuery('./static/RiskDB.db')
    if (str == ''):
        sql = "SELECT * FROM photo ORDER By time desc"
    else:
        sql = "SELECT * FROM photo WHERE description LIKE '%" + str + "%' ORDER By time desc"
    rq.instructions(sql)
    rq.do()
    record = '<p>My past photo</p>'
    for r in rq.format_results().split('\n\n'):
        record += '%s' % (make_html_paragraph(r))
    return record + '</table>\n'
