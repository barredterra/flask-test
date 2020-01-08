from flask import (Blueprint, redirect, request, url_for)
from flask_test import db

bp = Blueprint('api', __name__)

@bp.route('/<doc_type>', methods=['POST'])
def create_doc(doc_type):
    if doc_type == 'ProductMovement':
        print(request.form)
        required_fields = [(elem in request.form) for elem in ['to_location', 'qty', 'product']]
        if False not in required_fields:
            db.insert_movement(
                to_location=request.form['to_location'],
                from_location=request.form.get('from_location'),
                qty=request.form['qty'],
                product_id=request.form['product']
            )
    elif 'title' in request.form:
        db.insert_doc(doc_type, request.form.get('title'))

    return redirect(url_for('list.get_list', doc_type=doc_type))

@bp.route('/<doc_type>/<int:doc_id>/delete', methods=['GET', 'DELETE'])
def delete_doc(doc_type, doc_id):
    db.delete_doc(doc_type, doc_id)
    return redirect(url_for('list.get_list', doc_type=doc_type))
