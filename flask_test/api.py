import json
from flask import (Blueprint, Response, redirect, request, url_for)
from flask_test.db import Document
from flask_test.db import DocType

bp = Blueprint('api', __name__)

@bp.route('/resource/<doc_type>', methods=['POST'])
def create_doc(doc_type):
    if 'application/json' in request.headers.get('accept'):
        data = request.get_json()
    else:
        data = request.form

    dt = DocType(doc_type)
    dt.insert_doc(**data)
    return redirect(url_for('list.get', doc_type=doc_type))

@bp.route('/resource/<doc_type>/<doc_id>/delete', methods=['GET', 'DELETE'])
def delete_doc(doc_type, doc_id):
    doc = Document(doc_type, doc_id)
    doc.delete()
    return redirect(url_for('list.get', doc_type=doc_type))
