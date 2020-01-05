from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_test.db import get_db

bp = Blueprint('warehouse', __name__)

@bp.route('/<doc_type>', methods=['GET'])
def get_list(doc_type):
    return render_template('list.html', items=_get_list(doc_type), doc_type=doc_type)

@bp.route('/<doc_type>', methods=['POST'])
def create_doc(doc_type):
    if request.method == 'POST':
        title = request.form['title']
        if title:
            _insert_doc(doc_type, title)

    return redirect(url_for("warehouse.get_list", doc_type=doc_type))

@bp.route('/<doc_type>/<int:doc_id>', methods=['GET'])
def get_doc(doc_type, doc_id):
    doc = _get_doc(doc_type, doc_id)
    return render_template('single.html', doc=doc, doc_type=doc_type, locations=_get_list("Location"))

@bp.route('/<doc_type>/<int:doc_id>/<method>', methods=['POST', 'GET'])
def run_method(doc_type, doc_id, method):
    if doc_type == 'Product' and method == 'move':
        destination = request.form['destination']
        if destination:
            _move(doc_id, destination)

    if method == 'delete':
        _delete_doc(doc_type, doc_id)
        return redirect(url_for("warehouse.get_list", doc_type=doc_type))

    return redirect(url_for("warehouse.get_doc", doc_type=doc_type, doc_id=doc_id))

def _move(product_id, destination_id):
    print("Moving product {} to location {}".format(product_id, destination_id))
    doc = _get_doc('Product', product_id)

    source_id = None
    source = doc.get('location')
    if isinstance(source, dict):
        source_id = source.get('id')

    db = get_db()
    db.execute('INSERT INTO ProductMovement VALUES (?, ?, ?, ?, ?, ?)', (None, None, source_id, destination_id, product_id, 0))
    db.execute('UPDATE Product SET location = "%s" WHERE id = %d' % (destination_id, product_id))
    db.commit()

def _get_list(doc_type):
    db = get_db()
    doc_list = db.execute('SELECT * FROM %s' % doc_type)
    return doc_list.fetchall()

def _get_doc(doc_type, doc_id):
    db = get_db()
    results = db.execute('SELECT * FROM %s WHERE id = %d' % (doc_type, doc_id))
    doc = results.fetchone()
    
    if doc and doc.get('location'):
        doc['location'] = _get_doc("Location", int(doc.get('location')))

    return doc

def _insert_doc(doc_type, title):
    db = get_db()
    db.execute('INSERT INTO %s (title) VALUES (?)' % doc_type, [title])
    db.commit()

def _delete_doc(doc_type, doc_id):
    db = get_db()
    db.execute('DELETE FROM %s WHERE id = %d' % (doc_type, doc_id))
    db.commit()
