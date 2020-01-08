from flask import (Blueprint, render_template)
from flask_test import db

bp = Blueprint('single', __name__)

@bp.route('/<doc_type>/<int:doc_id>', methods=['GET'])
def get_doc(doc_type, doc_id):
    doc = db.get_doc(doc_type, doc_id)
    return render_template('single.html', doc=doc, doc_type=doc_type)
