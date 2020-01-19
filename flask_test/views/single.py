import json
from flask import (Blueprint, request, render_template)
from flask_test.db import Document
from flask_test.utils import row_as_json

bp = Blueprint('single', __name__)

@bp.route('/resource/<doc_type>/<doc_id>', methods=['GET'])
def get(doc_type, doc_id):
    doc = Document(doc_type, doc_id)
    data = doc.get()

    if 'application/json' in request.headers.get('accept'):
        return json.dumps(row_as_json(data))

    return render_template('single.html', doc=data, doc_type=doc_type)
