from flask import (Blueprint, render_template)
from flask_test import db
from flask_test.schema import FORM_SCHEMA

bp = Blueprint('list', __name__)

@bp.route('/resource/<doc_type>', methods=['GET'])
def get(doc_type):
    if doc_type == "Report":
        return render_template(
            'report.html',
            items=db.get_list(doc_type),
            doc_type=doc_type
        )

    return render_template(
        'list.html',
        items=db.get_list(doc_type),
        doc_type=doc_type,
        fields=FORM_SCHEMA[doc_type],
        get_options=db.get_list
    )
