import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import datetime
from flask_test.schema import FORM_SCHEMA

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
    return DocType(doc_type).get_list()

class DocType():
    def __init__(self, doc_type):
        self.doc_type = doc_type
        self.db = get_db()

    def get_list(self):
        doc_list = self.db.execute('SELECT * FROM %s' % self.doc_type)
        return doc_list.fetchall()

    def insert_doc(self, **kwargs):
        fields = self.db.execute(
            'SELECT field FROM DocFields WHERE doctype = ?',
            [self.doc_type]
        )
        fields_list = [f['field'] for f in fields.fetchall()]

        placeholders = ",".join("?" for i in range(len(fields_list)))
        fields_string = ",".join(fields_list)

        self.db.execute(
            "INSERT INTO %s (%s)" % (self.doc_type, fields_string) + "VALUES (%s)" % placeholders,
            [kwargs.get(field) for field in fields_list]
        )
        self.db.commit()


class Document():
    def __init__(self, doc_type):
        self.doc_type = doc_type
        self.db = get_db()

    def get(self, doc_id):
        results = self.db.execute('SELECT * FROM %s WHERE id = %d' % (self.doc_type, doc_id))
        return results.fetchone()

    def delete(self, doc_id):
        self.db.execute('DELETE FROM %s WHERE id = %d' % (self.doc_type, doc_id))
        self.db.commit()
