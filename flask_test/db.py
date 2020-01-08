import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import datetime


def get_db():
    """Return a database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """
    Close the database connection.
    
    - Check if a connection was created by checking if g.db was set.
    - If the connection exists, close it.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """Create the database tables."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# ---------------------- own ----------------------

def get_list(doc_type):
    db = get_db()
    doc_list = db.execute('SELECT * FROM %s' % doc_type)
    return doc_list.fetchall()

def get_doc(doc_type, doc_id):
    db = get_db()
    results = db.execute('SELECT * FROM %s WHERE id = %d' % (doc_type, doc_id))
    return results.fetchone()

def insert_doc(doc_type, title=None, from_location=None, to_location=None, product=None, qty=None):
    db = get_db()

    if doc_type == "ProductMovement":
        db.execute("""
            INSERT INTO %s (timestamp, from_location, to_location, product, qty)
            VALUES (?, ?, ?, ?, ?)
        """ % doc_type, [None, None, datetime.now().isoformat(), int(from_location), int(to_location), int(product), int(qty)])
    elif title:
        db.execute('INSERT INTO %s (title) VALUES (?)' % doc_type, [title])

    db.commit()

def insert_movement(to_location, product_id, qty, from_location=None):
    db = get_db()
    db.execute("""
        INSERT INTO ProductMovement (timestamp, from_location, to_location, product_id, qty)
        VALUES (?, ?, ?, ?, ?)
    """, [datetime.now().isoformat(), from_location, to_location, product_id, qty])
    db.commit()

def delete_doc(doc_type, doc_id):
    db = get_db()
    db.execute('DELETE FROM %s WHERE id = %d' % (doc_type, doc_id))
    db.commit()
