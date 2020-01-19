
def row_as_json(sqlite_row):
    """Return a dict from a sqlite_row."""
    return {
        key: sqlite_row[key]
        for key in sqlite_row.keys()
    }

def list_as_json(sqlite_rows):
    """Return a list of dicts from a list of sqlite_rows."""
    return [
        row_as_json(row)
        for row in sqlite_rows
    ]
