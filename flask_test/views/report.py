import json
from flask import (Blueprint, Response, request, render_template)
from flask_test import db
from flask_test.utils import list_as_json

bp = Blueprint('report', __name__)

@bp.route('/Report', methods=['GET'])
def get():
    data = db.get_list("Report")

    if 'application/json' in request.headers.get('accept'):
        response = json.dumps(list_as_json(data))
        return Response(response, mimetype="application/json")

    return render_template(
        'report.html',
        items=data,
        doc_type="Report"
    )
