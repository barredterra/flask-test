from flask import (Blueprint, redirect, request, url_for)
from flask_test.db import Document
from flask_test.db import DocType

bp = Blueprint('api', __name__)

@bp.route('/<doc_type>', methods=['POST'])
def create_doc(doc_type):
    dt = DocType(doc_type)
    dt.insert_doc(**request.form)
    return redirect(url_for('list.get', doc_type=doc_type))

@bp.route('/<doc_type>/<doc_id>/delete', methods=['GET', 'DELETE'])
def delete_doc(doc_type, doc_id):
    doc = Document(doc_type, doc_id)
    doc.delete()
    return redirect(url_for('list.get', doc_type=doc_type))
