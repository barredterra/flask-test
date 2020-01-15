from flask import (Blueprint, render_template)
from flask_test.db import Document

bp = Blueprint('single', __name__)

@bp.route('/<doc_type>/<int:doc_id>', methods=['GET'])
def get_doc(doc_type, doc_id):
    doc = Document(doc_type)
    return render_template('single.html', doc=doc.get(doc_id), doc_type=doc_type)
