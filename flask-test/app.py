from flask import Flask
from flask import request
from flask import abort, redirect, url_for
from flask import render_template
import sqlite3

app = Flask(__name__)

def dict_factory(cursor, row):
    """Convert SQL row to Python dict."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('flask-test.db')
conn.row_factory = dict_factory
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS
    Location (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title
    )
""")
c.execute("""
    CREATE TABLE IF NOT EXISTS
        Product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title,
            location
        )
""")
c.execute("""
    CREATE TABLE IF NOT EXISTS
        ProductMovement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            from_location INTEGER,
            to_location INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            qty
        )
""")
conn.commit()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/<doc_type>', methods=['GET'])
def get_list(doc_type):
    return render_template('list.html', items=_get_list(doc_type), doc_type=doc_type)

@app.route('/<doc_type>', methods=['POST'])
def create_doc(doc_type):
    if request.method == 'POST':
        title = request.form['title']
        if title:
            _insert_doc(doc_type, title)

    return redirect(url_for("get_list", doc_type=doc_type))

@app.route('/<doc_type>/<int:doc_id>', methods=['GET'])
def get_doc(doc_type, doc_id):
    doc = _get_doc(doc_type, doc_id)
    return render_template('single.html', doc=doc, doc_type=doc_type, locations=_get_list("Location"))

@app.route('/<doc_type>/<int:doc_id>/<method>', methods=['POST'])
def run_method(doc_type, doc_id, method):
    if doc_type == 'Product' and method == 'move':
        destination = request.form['destination']
        if destination:
            _move(doc_id, destination)
    
    return redirect(url_for("get_doc", doc_type=doc_type, doc_id=doc_id))

def _move(product_id, destination_id):
    print("Moving product {} to location {}".format(product_id, destination_id))
    doc = _get_doc('Product', product_id)

    source_id = None
    source = doc.get('location')
    if isinstance(source, dict):
        source_id = source.get('id')

    c.execute('INSERT INTO ProductMovement VALUES (?, ?, ?, ?, ?, ?)', (None, None, source_id, destination_id, product_id, 0))
    c.execute('UPDATE Product SET location = "%s" WHERE id = %d' % (destination_id, product_id))
    conn.commit()

def _get_list(doc_type):
    doc_list = c.execute('SELECT * FROM %s' % doc_type)
    return doc_list.fetchall()

def _get_doc(doc_type, doc_id):
    results = c.execute('SELECT * FROM %s WHERE id = %d' % (doc_type, doc_id))
    doc = results.fetchone()
    if doc.get('location'):
        doc['location'] = _get_doc("Location", int(doc.get('location')))

    return doc

def _insert_doc(doc_type, title):
    c.execute('INSERT INTO %s (title) VALUES (?)' % doc_type, [title])
    conn.commit()
