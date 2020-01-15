DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS ProductMovement;

CREATE TABLE Location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title
);

CREATE TABLE Product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title
);

CREATE TABLE ProductMovement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    from_location INTEGER,
    to_location INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    qty
);

CREATE TABLE DocFields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctype,
    field
);

INSERT INTO DocFields (doctype, field)
VALUES
    ("Location", "title"),
    ("Product", "title"),
    ("ProductMovement", "from_location"),
    ("ProductMovement", "to_location"),
    ("ProductMovement", "product_id"),
    ("ProductMovement", "qty");


CREATE VIEW Report AS
SELECT Location.title as Location, Product.title as Product, SUM(qty) as Stock
FROM ProductMovement

LEFT JOIN Product on Product.id = ProductMovement.product_id
LEFT JOIN Location on Location.id = ProductMovement.to_location

GROUP BY to_location, product_id;
