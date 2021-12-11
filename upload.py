# 谢铭轩
from flask import Blueprint,request
import datetime

from UseSqlite import InsertQuery

upload_bp = Blueprint("upload_bp", __name__)


@upload_bp.route("/", methods=['GET', 'POST'])
def upload():
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
        # page += get_database_photos()
        return page
