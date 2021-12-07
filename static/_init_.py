# -*- coding: utf-8 -*-
from flask import Flask
from test_blueprint import test_blueprint

app = Flask(__name__)
app.register_blueprint(test_blueprint)

