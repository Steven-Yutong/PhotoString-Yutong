# -*- coding: utf-8 -*-
from flask import Blueprint, request

test_blueprint = Blueprint('fir_blueprint', __name__)


@test_blueprint.route('/test', methods=['GET'])
def test():
    return "test success"
