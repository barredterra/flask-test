DROP TABLE IF EXISTS "Location";
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS ProductMovement;

CREATE TABLE Location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title
);

CREATE TABLE Product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title,
    "location" INTEGER,
    FOREIGN KEY ("location") REFERENCES Location(id)
);

CREATE TABLE ProductMovement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    from_location INTEGER,
    to_location INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    qty
);
