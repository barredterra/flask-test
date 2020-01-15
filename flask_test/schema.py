"""Fields for create form."""

FORM_SCHEMA = {
    "Product": [
        {
            "type": "text",
            "name": "title",
            "display": "Title"
        }
    ],
    "Location": [
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
            "options": "Location",
            "name": "from_location",
            "display": "From Location"
        },
        {
            "type": "select",
            "options": "Location",
            "name": "to_location",
            "display": "To Location"
        },
        {
            "type": "number",
            "name": "qty",
            "display": "Quantity"
        }
    ]
}
