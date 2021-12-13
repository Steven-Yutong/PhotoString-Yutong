# 吴雨桐 & 王炫 & 谢铭轩

from flask import Blueprint, request
from UseSqlite import InsertQuery, RiskQuery
from PIL import Image
import datetime

show_bp = Blueprint("show_bp", __name__)

# 定义项目的绝对路径
ch = 'E:/JupyterWork/PhotoString_by_ChenXintao'


# show:显示方法
@show_bp.route('/', methods=['GET', 'POST'])
def show():
    # 显示两个表单: 上传表单和检索表单
    # 点击上传表单的submit，跳转到上传的路由执行相应方法
    # 点击检索表单的submit，跳转到检索的路由执行指定条件的检索方法
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
    # 将数据库中的所有图片及其信息存到page中，输出到页面上
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


@show_bp.route("/upload", methods=['GET', 'POST'])  # 点击file跳转到/show/upload进行文件上传
def upload():

    uploaded_file = request.files['file']  # 获取文件
    time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 获取时间
    new_filename = time_str + '.jpg'  # 将新文件名称命名为当前时间
    uploaded_file.save(ch + '/static/upload/' + new_filename)  # 将新文件以当前时间命名，保存至static/upload文件夹下
    time_info = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取时间
    description = request.form['description']  # 获取文件名称
    path = ch + '/static/upload/' + new_filename  # 获取文件地址
    iq = InsertQuery(ch + '/static/RiskDB.db')  # 获取数据库地址
    iq.instructions(
        "INSERT INTO photo Values('%s','%s','%s','%s')" % (time_info, description, path, new_filename))  # 将文件信息存入数据库
    iq.do()
    return '<p>You have uploaded %s.<br/> <a href="/">Return</a>.' % (
        uploaded_file.filename)  # 显示文件upload成功，并增加返回show页面按钮。


# 将图片的信息转为网页显示的格式
# s为从数据库中读取的一张图片的一整条信息
def make_html_paragraph(s):
    if s.strip() == '':
        return ''
    lst = s.split(',')
    # 存储图片的路径
    picture_path = lst[2].strip()
    # 存储图片的名称
    picture_name = lst[3].strip()
    im = Image.open(picture_path)
    # 存储图片的缩略图格式
    im.thumbnail((400, 300))
    im.save('./static/figure/' + picture_name, 'jpeg')
    # 将信息存为网页形式
    result = '<p>'
    result += '<i>%s</i><br/>' % (lst[0])
    result += '<i>%s</i><br/>' % (lst[1])
    result += '<a href="%s"><img src="/static/figure/%s"alt="风景图"></a>' % (picture_path, picture_name)
    return result + '</p>'


# 获取数据库所有照片及其信息
def get_database_photos(str=''):
    rq = RiskQuery('./static/RiskDB.db')
    # sql语句:无检索特殊要求，默认检索所有图片
    if (str == ''):
        sql = "SELECT * FROM photo ORDER By time desc"
    # sql语句:有特殊检索要求:str, 以str为关键字检索所有与之相关的图片
    else:
        sql = "SELECT * FROM photo WHERE description LIKE '%" + str + "%' ORDER By time desc"
    rq.instructions(sql)
    rq.do()
    record = '<p>My past photo</p>'
    # 将读取到的sql语句转化为网页输出形式
    for r in rq.format_results().split('\n\n'):
        record += '%s' % (make_html_paragraph(r))
    return record + '</table>\n'
