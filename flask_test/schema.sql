DROP TABLE IF EXISTS Warehouse;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS ProductMovement;

CREATE TABLE Warehouse (
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
    from_warehouse INTEGER,
    to_warehouse INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    qty
);

CREATE TABLE DocFields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctype,
    field
);

CREATE VIEW Report AS
WITH
incoming AS (
    SELECT
        to_warehouse as warehouse,
        product_id,
        SUM(qty) as amount
    FROM ProductMovement
    WHERE to_warehouse IS NOT NULL
    GROUP BY product_id, to_warehouse
),
outgoing AS (
    SELECT
        from_warehouse as warehouse,
        product_id,
        -SUM(qty) as amount
    FROM ProductMovement
    WHERE from_warehouse IS NOT NULL
    GROUP BY product_id, from_warehouse
)
SELECT
    Warehouse.title as warehouse,
    Product.title as product,
    SUM(amount) as stock
FROM (
    SELECT warehouse, product_id, amount FROM incoming
    UNION ALL
    SELECT warehouse, product_id, amount FROM outgoing
)
LEFT JOIN Warehouse ON
Warehouse.id = warehouse
LEFT JOIN Product ON
Product.id = product_id
GROUP BY warehouse, product_id;


INSERT INTO DocFields (doctype, field)
VALUES
    ("Warehouse", "title"),
    ("Product", "title"),
    ("ProductMovement", "from_warehouse"),
    ("ProductMovement", "to_warehouse"),
    ("ProductMovement", "product_id"),
    ("ProductMovement", "qty");

INSERT INTO Warehouse (title)
VALUES
    ("Mumbai"),
    ("Berlin"),
    ("New York");

INSERT INTO Product (title)
VALUES
    ("Banana"),
    ("iPhone"),
    ("Printer");
