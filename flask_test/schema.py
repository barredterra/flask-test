"""Fields for create form."""

FORM_SCHEMA = {
    "Product": [
        {
            "type": "text",
            "name": "title",
            "display": "Title"
        }
    ],
    "Warehouse": [
        {
            "type": "text",
            "name": "title",
            "display": "Title"
        }
    ],
    "ProductMovement": [
        {
            "type": "select",
            "options": "Product",
            "name": "product_id",
            "display": "Product"
        },
        {
            "type": "select",
            "options": "Warehouse",
            "name": "from_warehouse",
            "display": "From Warehouse"
        },
        {
            "type": "select",
            "options": "Warehouse",
            "name": "to_warehouse",
            "display": "To Warehouse"
        },
        {
            "type": "number",
            "name": "qty",
            "display": "Quantity"
        }
    ]
}
