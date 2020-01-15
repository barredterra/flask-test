from flask import (Blueprint, redirect, request, url_for)
from flask_test import db

bp = Blueprint('api', __name__)

@bp.route('/<doc_type>', methods=['POST'])
def create_doc(doc_type):
    db.insert_doc(doc_type, **request.form)
    return redirect(url_for('list.get_list', doc_type=doc_type))

@bp.route('/<doc_type>/<int:doc_id>/delete', methods=['GET', 'DELETE'])
def delete_doc(doc_type, doc_id):
    db.delete_doc(doc_type, doc_id)
    return redirect(url_for('list.get_list', doc_type=doc_type))
