from flask import (Blueprint, render_template)
from flask_test import db

bp = Blueprint('report', __name__)

@bp.route('/Report', methods=['GET'])
def get():
    return render_template(
        'report.html',
        items=db.get_list("Report"),
        doc_type="Report"
    )
